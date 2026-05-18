import logging
from dataclasses import dataclass, field
from typing import Any

from trame.widgets import gwc, html
from trame.widgets import vuetify3 as v3
from trame_server.utils.typed_state import TypedState
from undo_stack import Signal

logger = logging.getLogger(__name__)


@dataclass
class GirderDownloads:
    file_name: str
    number_of_downloads: int = 0


@dataclass
class GirderBrowserState:
    downloaded_items: list[GirderDownloads] = field(default_factory=list)
    location: dict[str, str] | None = None
    is_browser_dialog_visible: bool = False
    is_search_dialog_visible: bool = False
    is_downloading: bool = False


class GirderBrowserUI(html.Div):
    row_clicked = Signal(dict[str, Any])
    location_updated = Signal(dict[str, Any])

    def __init__(self, **kwargs):
        super().__init__(classes="d-flex", **kwargs)
        self._typed_state = TypedState(self.state, GirderBrowserState)
        self._build_ui()

    def _close(self):
        self._typed_state.data.is_browser_dialog_visible = False

    def _build_ui(self):
        with self:
            with v3.VDialog(
                v_model=(self._typed_state.name.is_browser_dialog_visible,),
                activator="parent",
                width=800,
            ):
                with v3.Template(v_slot_activator="{ props : activatorProps }"):
                    v3.VBtn(v_bind="activatorProps", icon="mdi-file-plus-outline")

                with v3.VCard(title="Select data"):
                    with v3.VCardText(classes="pa-0"):
                        gwc.GirderFileManager(
                            v_if=(self._typed_state.name.location,),
                            location=(self._typed_state.name.location,),
                            update_location=(self.location_updated, "[$event]"),
                            row_click=(self.row_clicked, "[$event]"),
                            style="width: 100%",
                        )
                    with v3.VCardActions(classes="justify-end"):
                        v3.VBtn(text="Done", variant="tonal", click=self._close)
