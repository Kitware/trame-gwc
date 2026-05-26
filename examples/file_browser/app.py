from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import client, html
from trame.widgets import vuetify3 as v3
from trame_server import Server

from widgets.logic.girder_browser_logic import GirderBrowserLogic
from widgets.logic.girder_connection_logic import GirderConnectionLogic
from widgets.ui.girder_browser_ui import GirderBrowserUI
from widgets.ui.girder_connection_ui import GirderConnectionUI


class TrameGWCApp(TrameApp):
    def __init__(self, server: Server | None, **kwargs) -> None:
        super().__init__(server, **kwargs)
        layout = VAppLayout(self.server)
        self._girder_connection_logic = GirderConnectionLogic(
            self.server, default_url="https://data.kitware.com"
        )
        self._girder_browser_logic = GirderBrowserLogic(
            self.server, self._girder_connection_logic.girder_client
        )

        self._girder_connection_logic.girder_client_changed.connect(
            self._girder_browser_logic.set_client
        )
        self._girder_connection_logic.girder_user_changed.connect(
            self._girder_browser_logic.set_location_to_default
        )

        self.state.trame__title = "trame-gwc demo app"

        with layout:
            client.Style(
                "html { overflow-y: hidden; } "
                ".text-header { padding-bottom: 8px; font-size: 1.125rem; font-weight: 300; "
                "line-height: 1.6; letter-spacing: 0.0125em;}"
            )
            self._girder_connection_logic.provider.register_layout(layout)
            with v3.VAppBar(height=75):
                with v3.Template(v_slot_prepend=True):
                    self.girder_browser_ui = GirderBrowserUI()

                v3.VAppBarTitle(self.state.trame__title, style="flex: 0 1 auto;")
                v3.VSpacer()
                self.girder_connection_ui = GirderConnectionUI()

            with v3.VMain(), html.Div(classes="pa-2"):
                html.Div(
                    "Connected as {{ "
                    + self._girder_connection_logic.name.girder_user_name
                    + " }}",
                    v_if=(self._girder_connection_logic.name.girder_user_name,),
                    classes="py-2 text-header",
                )
                html.Div("Not connected", v_else=True, classes="py-2 text-header")
                v3.VDivider()
                with html.Div(classes="d-flex align-center"):
                    html.Div("Downloaded items", classes="py-2 text-header")
                    v3.VProgressCircular(
                        v_if=(self._girder_browser_logic.name.is_downloading,),
                        classes="ml-4",
                        indeterminate=True,
                        size="small",
                    )

                with v3.VList(
                    v_if=(f"{self._girder_browser_logic.name.downloaded_items}.length")
                ):
                    v3.VListItem(
                        v_for=f"downloaded_item in {self._girder_browser_logic.name.downloaded_items}",
                        title=("downloaded_item.file_name",),
                        subtitle=(
                            "`Downloaded ${downloaded_item.number_of_downloads} times`",
                        ),
                    )
                html.Div(
                    "No items downloaded yet...", v_else=True, classes="font-italic"
                )

        self._girder_connection_logic.set_ui(self.girder_connection_ui)
        self._girder_browser_logic.set_ui(self.girder_browser_ui)


def main(server=None, **kwargs):
    app = TrameGWCApp(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
