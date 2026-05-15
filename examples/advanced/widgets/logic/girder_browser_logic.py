import logging
from pathlib import Path
from time import time
from typing import Any

from girder_client import GirderClient
from trame.app import asynchronous
from trame_server import Server

from ..ui.girder_browser_ui import GirderDownloads, GirderBrowserState, GirderBrowserUI
from .base_logic import BaseLogic

logger = logging.getLogger(__name__)


class GirderBrowserLogic(BaseLogic[GirderBrowserState]):
    girder_client: GirderClient | None = None

    def __init__(
        self,
        server: Server,
        default_location: dict[str, str] | None = None,
    ) -> None:
        super().__init__(server, GirderBrowserState)
        self._last_clicked = 0
        self._downloaded_items: dict[str, GirderDownloads] = {}

        self._default_location = (
            default_location if default_location is not None else {"type": "root"}
        )
        self._set_location(self._default_location)

    def set_ui(self, browser_ui: GirderBrowserUI) -> None:
        browser_ui.row_clicked.connect(self._click_item)
        browser_ui.location_updated.connect(self._set_location)

    def set_client(self, girder_client: GirderClient | None):
        self.girder_client = girder_client

    def set_location_to_default(self, *args):
        self._set_location(self._default_location)

    @asynchronous.task
    async def _download_item(self, item: dict[str, Any]):
        if self.girder_client is not None:
            with self.state:
                self.data.is_downloading = True
            await self.server.network_completion

            if item["_id"] not in self._downloaded_items:
                self._downloaded_items[item["_id"]] = GirderDownloads(item["name"])

            try:
                download_path = Path.cwd() / item["name"]
                self.girder_client.downloadItem(item["_id"], str(download_path))
                self._downloaded_items[item["_id"]].number_of_downloads += 1

            finally:
                if self._downloaded_items[item["_id"]].number_of_downloads == 0:
                    self._downloaded_items.pop(item["_id"])
                self.data.downloaded_items = list(self._downloaded_items.values())

            with self.state:
                self.data.is_downloading = False
            await self.server.network_completion

    def _click_item(self, item: dict[str, Any]) -> None:
        if item.get("_modelType") != "item":
            return

        # Ignore double click on item
        clicked_time = time()
        if clicked_time - self._last_clicked < 1:
            return
        self._last_clicked = clicked_time

        logger.debug(f"Item {item['_id']} clicked")
        self._download_item(item)

    def _set_location(self, location: dict[str, Any] | None) -> None:
        new_location = None
        if location is not None:
            location_type = location.get("type")
            location_id = location.get("_id")
            location_model_type = location.get("_modelType")
            if location_id is not None and location_model_type is not None:
                logger.debug(f"Location changed to {location_id}")
                new_location = {"_id": location_id, "_modelType": location_model_type}
            elif location_type is not None:
                logger.debug(f"Location changed to {location_type}")
                new_location = location

        self.data.location = new_location
