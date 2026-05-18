import logging
from typing import Any
from urllib.parse import urljoin

from girder_client import GirderClient
from undo_stack import Signal
from trame.widgets.gwc import GirderProvider
from trame_server import Server

from ..ui.girder_connection_ui import GirderConnectionState, GirderConnectionUI
from ..utils import is_valid_url
from .base_logic import BaseLogic

logger = logging.getLogger(__name__)


class GirderConnectionLogic(BaseLogic[GirderConnectionState]):
    girder_client_changed = Signal(GirderClient | None)
    girder_user_changed = Signal()
    girder_client: GirderClient | None = None

    def __init__(
        self, server: Server, default_url: str | None, default_api_root: str = "/api/v1"
    ) -> None:
        super().__init__(server, GirderConnectionState)
        self.provider = GirderProvider(
            trame_server=self.server,
            api_root=(self.name.api_url,),
            user_logged_in=(self._login, "[$event.user, $event.token]"),
            fetch_user=(self._login, "[$event.user, $event.token]"),
        )
        self.api_root = default_api_root
        self.data.girder_url = default_url

        self.bind_changes(
            {
                (self.name.api_url,): self._on_api_url_changed,
                (self.name.girder_url,): self._on_girder_url_changed,
            }
        )

    def set_ui(self, connection_ui: GirderConnectionUI) -> None:
        connection_ui.log_out_clicked.connect(self._logout)

    def _load_girder(self) -> None:
        if self.data.girder_url:
            api_url = (
                urljoin(self.data.girder_url, self.api_root)
                if self.data.girder_url
                else None
            )
            valid_url, self.data.url_error = is_valid_url(api_url)
            if valid_url:
                self.data.api_url = api_url

    def _connect_girder(self, api_url: str | None) -> None:
        self.provider.connect(api_url)
        self.girder_client = GirderClient(apiUrl=api_url)
        self.girder_client_changed(self.girder_client)

    def _disconnect_girder(self) -> None:
        self._logout()
        self.provider.disconnect()
        self.girder_client = None
        self.girder_client_changed(None)

    def _on_api_url_changed(self, api_url: str | None) -> None:
        if api_url is None:
            self._disconnect_girder()
        else:
            self._connect_girder(api_url)

    def _on_girder_url_changed(self, girder_url: str | None) -> None:
        self.data.api_url = None

        if girder_url:
            self._load_girder()
        else:
            self.data.url_error = "URL required"

    def _login(self, info: dict[str, Any] | None, token: str | None) -> None:
        if info is not None and token is not None:
            self.data.girder_user_name = (
                f"{info.get('firstName', None)} {info.get('lastName', None)}"
            )
            self.data.is_login_dialog_visible = False

            if self.girder_client is not None:
                self.girder_client.setToken(token)

            self.girder_user_changed()

    def _logout(self) -> None:
        if self.data.girder_user_name:
            self.provider.logout()
            self.data.girder_user_name = None

            if self.girder_client is not None:
                self.girder_client.setToken(None)

            self.girder_user_changed()
