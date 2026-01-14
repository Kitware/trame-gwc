from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.decorators import change
from trame.widgets import gwc, html
from trame.widgets import vuetify3 as vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------


class GWCDemoApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.provider = None
        self.state.update(
            {
                "theme": "dark",
                "api_root": "https://data.kitware.com/api/v1",
                "auth_register": True,
                "new_folder_enabled": True,
                "root_location_disabled": False,
                "selectable": True,
                "selected": [],
                "upload_enabled": True,
                "upload_multiple": True,
                "upsert_edit": False,
                "user": None,
                "location": None,
                "upsert_dest": None,
                "upload_dest": None,
                "path": None,
            }
        )
        self._build_ui()

    @change("api_root")
    def _set_api_root(self, api_root, **_kwargs):
        if self.provider is not None:
            if api_root:
                self.provider.connect(api_root)
            else:
                self.provider.disconnect()

    @change("user")
    def _set_user(self, user, **_kwargs):
        self.state.firstName = user.get("firstName", "").capitalize() if user else None
        self.state.lastName = user.get("lastName", "").upper() if user else None
        if user is not None:
            self.state.location = user

    @change("location")
    def _set_upload_dest(self, location, **_kwargs):
        # Define upload_dest only when the location is a folder
        if location and location.get("_modelType") == "folder":
            self.state.upload_dest = location
        else:
            self.state.upload_dest = None

    @change("location")
    def _set_upsert_dest(self, location, **_kwargs):
        if location and location.get("_modelType") in ["folder", "user"]:
            self.state.upsert_dest = location
        else:
            self.state.upsert_dest = None

    @change("location", "selected")
    def _set_data_details(self, location, selected, **_kwargs):
        if selected:
            self.state.data_details = selected
        elif location and location.get("_id", ""):
            self.state.data_details = [location]
        else:
            self.state.data_details = []

    def _update_location(self, new_location):
        self.state.location = new_location

    def _update_selected(self, new_selected):
        self.state.selected = new_selected

    def _handle_search_select(self, item):
        model_type = item.get("_modelType")
        if item and model_type in ["user", "folder", "collection"]:
            self.state.location = item
        elif model_type == "item":
            self.state.location = {"_modelType": "folder", "_id": item["folderId"]}

    def _handle_action(self, action):
        if action.name == "Delete":
            self.state.selected = []

    def _build_ui(self):
        with VAppLayout(self.server, theme=("theme",)) as self.layout:
            with gwc.GirderProvider(
                api_root=("api_root",),
                user_logged_in="user = $event.user;",
                user_logged_out="user = null; location = null;",
                user_registered="user = $event.user;",
            ) as self.provider:
                with vuetify.VContainer():
                    with vuetify.VRow():
                        with vuetify.VCol(cols=10):
                            html.Div(
                                "Girder Web Components for Trame",
                                classes="text-h5 display-3",
                            )
                        with vuetify.VCol(cols=2):
                            vuetify.VSwitch(
                                v_model=("theme"),
                                value="dark",
                                false_value="light",
                                classes="mx-4 my-0",
                                hide_details="hide-details",
                                label="Dark theme",
                            )

                    with html.Div(classes="text-body-1 mb-1"):
                        html.Span("A Trame library using the Vue")
                        html.A(
                            "Girder Web Components",
                            href="https://gwc.girder.org/",
                            target="_blank",
                        )
                        html.Span("for interacting with")
                        html.A(
                            "data.kitware.com",
                            href="https://data.kitware.com",
                            target="_blank",
                        )
                        html.Span("data management platform,")
                        html.A(
                            "Girder",
                            href="https://girder.readthedocs.io/en/stable/",
                            target="_blank",
                        )
                    with html.Div(classes="text-body-1 mb-1"):
                        html.Span("This demo integrates with ")
                        html.A(
                            "data.kitware.com",
                            href="https://data.kitware.com",
                            target="_blank",
                        )

                with (
                    vuetify.VContainer(v_if=("!api_root",)),
                    vuetify.VForm(
                        submit_prevent="api_root = path",
                        __events=[("submit_prevent", "submit.prevent")],
                    ),
                    vuetify.VTextField(
                        v_model=("path",),
                        label="Girder API Root",
                        variant="solo-filled",
                        clearable=True,
                    ),
                    vuetify.Template(v_slot_append=True),
                ):
                    vuetify.VBtn(icon="mdi-chevron-right", type="submit")

                with vuetify.VContainer(v_else=True):
                    with vuetify.VRow():
                        with vuetify.VCol(cols=10):
                            with html.Div(classes="subtitle-1 mb-1"):
                                html.Span("Connected to")
                                html.A(
                                    "{{ api_root }}",
                                    href=("api_root",),
                                    target="_blank",
                                )
                        with vuetify.VCol(cols=2):
                            vuetify.VBtn(
                                "Disconnect",
                                click="api_root = null;",
                                block=True,
                                color="primary",
                            )

                    # AUTHENTICATION
                    with html.Div():
                        with html.Div(v_if=("!user",)):
                            Headline(
                                title="girder-authentication",
                                link="src/components/Authentication/Authentication.vue",
                                description="allows users to authenticate with girder",
                            )
                            vuetify.VSwitch(
                                v_model=("auth_register",),
                                label="Register",
                            )
                            gwc.GirderAuthentication(register=("auth_register",))

                        with vuetify.VRow(v_else=True):
                            with vuetify.VCol(cols=10):
                                html.Div(
                                    "Welcome {} {}".format(
                                        "{{ firstName }} ", "{{ lastName }} "
                                    ),
                                    classes="subtitle-1 mb-1",
                                )
                            with vuetify.VCol(cols=2):
                                vuetify.VBtn(
                                    "Log Out",
                                    click=self.provider.logout,
                                    block=True,
                                    color="primary",
                                )

                    # SEARCH
                    with html.Div():
                        Headline(
                            title="girder-search",
                            link="src/components/Search.vue",
                            description="provides global search functionality",
                        )
                        with vuetify.VCard(classes="pa-3"):
                            gwc.GirderSearch(
                                select=(
                                    self._handle_search_select,
                                    "[$event]",
                                )
                            )

                    # FILEMANAGER AND DATADETAILS
                    with vuetify.VRow():
                        with vuetify.VCol(xl=8, lg=8, md=6, sm=12):
                            Headline(
                                title="girder-file-manager",
                                link="src/components/snippets/FileManager.vue",
                                description="a wrapper around girder-data-browser. \
                                    It packages the browser with defaults including folder creation, \
                                    item upload, and a breadcrumb bar",
                            )
                        with vuetify.VCol(xl=4, lg=4, md=6, sm=12):
                            Headline(
                                title="girder-data-details",
                                link="src/components/DataDetails.vue",
                                description="in-depth information and controls for a single \
                                    folder or item, or batch operations for groups of objects",
                            )

                    with html.Div(v_if=("location",)):
                        with html.Div(classes="d-flex justify-space-around"):
                            vuetify.VSwitch(
                                v_model=("selectable",),
                                label="Select",
                            )
                            vuetify.VSwitch(
                                v_model=("new_folder_enabled",),
                                label="New Folder",
                            )
                            vuetify.VSwitch(
                                v_model=("upload_enabled",),
                                label="Upload",
                            )
                            vuetify.VSwitch(
                                v_model=("root_location_disabled",),
                                label="Root Disabled",
                            )

                        with vuetify.VRow():
                            with vuetify.VCol(xl=8, lg=8, md=6, sm=12):
                                gwc.GirderFileManager(
                                    location=("location",),
                                    update_location=(
                                        self._update_location,
                                        "[$event]",
                                    ),
                                    selected=("selected",),
                                    update_selected=(
                                        self._update_selected,
                                        "[$event]",
                                    ),
                                    selectable=("selectable",),
                                    root_location_disabled=("root_location_disabled",),
                                    upload_enabled=("upload_enabled",),
                                    new_folder_enabled=("new_folder_enabled",),
                                )

                            with vuetify.VCol(xl=4, lg=4, md=6, sm=12):
                                gwc.GirderDataDetails(
                                    value=("data_details",),
                                    action=(self._handle_action, "[$event]"),
                                )

                    with html.Div(
                        v_else=True,
                        classes="d-flex text-body-2 justify-center font-italic",
                    ):
                        html.Span(
                            "Login or search for a folder/user/collection "
                            "to display the file manager and the data details component"
                        )

                    # # JOB LIST
                    # with vuetify.VRow(), vuetify.VCol(cols=12):
                    #     Headline(
                    #         title="girder-job-list",
                    #         link="src/components/Job/JobList.vue",
                    #         description="display and filter girder jobs",
                    #     )
                    #     gwc.GirderJobList()

                    # UPLOAD
                    with html.Div():
                        Headline(
                            title="girder-upload",
                            link="src/components/Upload.vue",
                            description="upload files to a specified location in girder",
                        )
                        gwc.GirderUpload(v_if=("upload_dest",), dest=("upload_dest",))
                        with html.Div(
                            v_else=True,
                            classes="d-flex text-body-2 justify-center font-italic",
                        ):
                            html.Span(
                                "Login or search for a folder to display the upload component"
                            )

                    # ACCESS CONTROL
                    with html.Div():
                        Headline(
                            title="girder-access-control",
                            link="src/components/AccessControl.vue",
                            description="access controls for folders and items",
                        )
                        gwc.GirderAccessControl(
                            v_if=("upsert_dest",), model=("upsert_dest",)
                        )
                        with html.Div(
                            v_else=True,
                            classes="d-flex text-body-2 justify-center font-italic",
                        ):
                            html.Span(
                                "Login or search for a folder/user to display the access control component"
                            )

                    # EDIT/ADD FOLDER
                    with html.Div():
                        Headline(
                            title="girder-upsert-folder",
                            link="src/components/UpsertFolder.vue",
                            description="create and edit folders",
                        )
                        with html.Div(v_if=("upsert_dest",)):
                            vuetify.VSwitch(
                                v_model=("upsert_edit",),
                                label="Edit Mode",
                            )
                            gwc.GirderUpsertFolder(
                                location=("upsert_dest",), edit=("upsert_edit",)
                            )

                        with html.Div(
                            v_else=True,
                            classes="d-flex text-body-2 justify-center font-italic",
                        ):
                            html.Span(
                                "Login or search for a folder/user to display the upsert folder component"
                            )

                    # BREADCRUMB
                    with html.Div():
                        Headline(
                            title="girder-breadcrumb",
                            link="src/components/Breadcrumb.vue",
                            description="filesystem path breadcrumb",
                        )
                        with vuetify.VCard(v_if=("location",), classes="pa-3"):
                            gwc.GirderBreadcrumb(
                                location=("location",),
                                root_location_disabled=("root_location_disabled",),
                            )
                        with html.Div(
                            v_else=True,
                            classes="d-flex text-body-2 justify-center font-italic",
                        ):
                            html.Span(
                                "Login or search for a folder/user/collection to display the breadcrumb component"
                            )


class Headline(html.Div):
    REPO_BASE = "https://github.com/girder/girder_web_components/blob/master/"

    def __init__(self, title, description, link):
        super().__init__(classes="my-3")
        with self:
            with html.Div(title, classes="text-h6"):
                vuetify.VBtn(
                    href=Headline.REPO_BASE + link,
                    icon="mdi-open-in-new",
                    classes="ml-2",
                    title="View Source",
                    target="_blank",
                    variant="text",
                )
            html.Div(description, classes="text-subtitle-1")


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = GWCDemoApp()
    app.server.start()
