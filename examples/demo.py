from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from trame.widgets import gwc, html
from trame.widgets import vuetify2 as vuetify
import os

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller
state.update(
    {
        "api_root": os.environ.get(
            "TRAME_APP_API_ROOT", "https://data.kitware.com/api/v1"
        ),
        "auth_register": True,
        "new_folder_enabled": True,
        "root_location_disabled": False,
        "selectable": True,
        "selected": [],
        "upload_enabled": True,
        "upload_multiple": True,
        "upsert_edit": False,
        "user": None,
    }
)


# -----------------------------------------------------------------------------
# API connection
# -----------------------------------------------------------------------------


def disconnect():
    state.api_root = None
    state.path = None
    state.user = None


def connect():
    state.api_root = state.path


# -----------------------------------------------------------------------------
# Data management
# -----------------------------------------------------------------------------


@state.change("user")
def set_user(user, **kwargs):
    state.firstName = user.get("firstName", "").capitalize() if user else None
    state.lastName = user.get("lastName", "").upper() if user else None
    state.location = user if user else None


@state.change("location")
def set_upload_dest(location, **kwargs):
    # Define upload_dest only when the location is a folder or a user
    if location and location.get("_modelType") == "folder":
        state.upload_dest = location
    elif location and location.get("_modelType") == "user":
        state.upload_dest = {**location, "name": location.get("login", "")}
    else:
        state.upload_dest = None


@state.change("location", "selected")
def set_data_details(**kwargs):
    if state.selected:
        state.data_details = state.selected
    elif state.location and state.location.get("_id", ""):
        state.data_details = [state.location]
    else:
        state.data_details = []


def update_location(new_location):
    state.location = new_location


def handle_search_select(item, **kwargs):
    if item and item.get("_modelType") in ["user", "folder"]:
        state.location = item
    else:
        state.location = {"_modelType": "folder", "_id": item.folderId}


def handle_action(action, **kwargs):
    if action.name == "Delete":
        state.selected = []


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------


class Headline:
    REPO_BASE = "https://github.com/girder/girder_web_components/blob/master/"

    def __init__(self, title, description, link):
        with html.Div():
            with html.Div(title, classes="headline font-weight-bold mono mt-8"):
                with vuetify.VBtn(
                    href=Headline.REPO_BASE + link,
                    icon="icon",
                    classes="ml-2",
                    title="View Source",
                    target="_blank",
                ):
                    vuetify.VIcon("mdi-open-in-new")
            html.Div(description, classes="subtitle-1 mb-4")


with VAppLayout(server) as layout:
    with vuetify.VContainer():
        html.Div("Girder Web Components for Trame", classes="display-3")
        with html.Div(classes="title mb-1"):
            html.Span("A Trame library using the Vue")
            html.A(
                "Girder Web Components", href="https://gwc.girder.org/", target="_blank"
            ),
            html.Span("for interacting with")
            html.A("data.kitware.com", href="https://data.kitware.com", target="_blank")
            html.Span("data management platform,")
            html.A(
                "Girder",
                href="https://girder.readthedocs.io/en/stable/",
                target="_blank",
            )

        with vuetify.VRow():
            with vuetify.VCol(cols=10):
                with html.Div(classes="title mb-1"):
                    html.Span("This demo integrates with "),
                    html.A(
                        "data.kitware.com",
                        href="https://data.kitware.com",
                        target="_blank",
                    )
            with vuetify.VCol(cols=2, align="end"):
                vuetify.VSwitch(
                    v_model="$vuetify.theme.dark",
                    classes="mx-4 my-0",
                    hide_details="hide-details",
                    label="Dark theme",
                )

    with vuetify.VContainer(v_if=("!api_root",)):
        vuetify.VTextField(
            v_model=("path",),
            label="Girder API Root",
            type="input",
            filled=True,
            clearable=True,
            append_icon="mdi-chevron-right",
            click_append=connect,
        )

    with vuetify.VContainer(v_if=("api_root",)):
        with vuetify.VRow():
            with vuetify.VCol(cols=10):
                with html.Div(classes="subtitle-1 mb-1"):
                    html.Span("Connected to"),
                    html.A("{{ api_root }}", href=("api_root",), target="_blank")
            with vuetify.VCol(cols=2):
                vuetify.VBtn(
                    "Disconnect",
                    click=disconnect,
                    block=True,
                    color="primary",
                )

    with gwc.GirderProvider(v_if=("api_root",)) as provider:
        # AUTHENTICATION
        with vuetify.VContainer(v_if=("!user",)):
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

        with vuetify.VContainer(v_else=True):
            with vuetify.VRow():
                with vuetify.VCol(cols=10):
                    html.Div(
                        "Welcome {} {}".format("{{ firstName }} ", "{{ lastName }} "),
                        classes="subtitle-1 mb-1",
                    )
                with vuetify.VCol(cols=2):
                    vuetify.VBtn(
                        "Log Out",
                        click=provider.logout,
                        block=True,
                        color="primary",
                    )

            # SEARCH
            with vuetify.VRow(), vuetify.VCol(cols=12):
                Headline(
                    title="girder-search",
                    link="src/components/Search.vue",
                    description="provides global search functionality",
                )
                with vuetify.VToolbar(color="primary"):
                    gwc.GirderSearch(
                        select=(
                            handle_search_select,
                            "[$event]",
                        )
                    )

            # FILEMANAGER AND DATADETAILS
            with vuetify.VRow():
                with vuetify.VCol(cols=7):
                    Headline(
                        title="girder-file-manager",
                        link="src/components/snippets/FileManager.vue",
                        description="a wrapper around girder-data-browser. \
                            It packages the browser with defaults including folder creation, \
                            item upload, and a breadcrumb bar",
                    )
                with vuetify.VCol(cols=5):
                    Headline(
                        title="girder-data-details",
                        link="src/components/DataDetails.vue",
                        description="in-depth information and controls for a single \
                            folder or item, or batch operations for groups of objects",
                    )

            with vuetify.VRow():
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
                with vuetify.VCol(cols=7):
                    gwc.GirderFileManager(
                        v_model=("selected",),
                        location=("location",),
                        update_location=(update_location, "[$event]"),
                        selectable=("selectable",),
                        root_location_disabled=("root_location_disabled",),
                        upload_enabled=("upload_enabled",),
                        new_folder_enabled=("new_folder_enabled",),
                    )

                with vuetify.VCol(cols=5):
                    gwc.GirderDataDetails(
                        value=("data_details",), action=(handle_action, "[$event]")
                    )

            # JOB LIST
            with vuetify.VRow(), vuetify.VCol(cols=12):
                Headline(
                    title="girder-job-list",
                    link="src/components/Job/JobList.vue",
                    description="display and filter girder jobs",
                )
                gwc.GirderJobList()

            # UPLOAD
            with vuetify.VRow(v_if=("upload_dest",)), vuetify.VCol(cols=12):
                Headline(
                    title="girder-upload",
                    link="src/components/Upload.vue",
                    description="upload files to a specified location in girder",
                )
                with vuetify.VCard():
                    gwc.GirderUpload(dest=("upload_dest",))

            # ACCESS CONTROL
            with vuetify.VRow(v_if=("upload_dest",)), vuetify.VCol(cols=12):
                Headline(
                    title="girder-access-control",
                    link="src/components/AccessControl.vue",
                    description="access controls for folders and items",
                )
                gwc.GirderAccessControl(model=("upload_dest",))

            # EDIT/ADD FOLDER
            with vuetify.VRow(v_if=("upload_dest",)), vuetify.VCol(cols=12):
                Headline(
                    title="girder-upsert-folder",
                    link="src/components/UpsertFolder.vue",
                    description="create and edit folders",
                )
                vuetify.VSwitch(
                    v_model=("upsert_edit",),
                    label="Edit Mode",
                )
                with vuetify.VCard():
                    gwc.GirderUpsertFolder(
                        location=("upload_dest",), edit=("upsert_edit",)
                    )

            # BREADCRUMB
            with vuetify.VRow(v_if=("upload_dest",)), vuetify.VCol(cols=12):
                Headline(
                    title="girder-breadcrumb",
                    link="src/components/Breadcrumb.vue",
                    description="filesystem path breadcrumb",
                )
                with vuetify.VCard(classes="pa-4"):
                    gwc.GirderBreadcrumb(
                        location=("upload_dest",),
                        root_location_disabled=("root_location_disabled",),
                    )


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
