from trame.app import get_server
from trame.ui.vuetify import VAppLayout
from generic_components import Headline
from trame.widgets import gwc, html
from trame.widgets import vuetify2 as vuetify
import os

# Initialize server
server = get_server(client_type = 'vue2')
state, ctrl = server.state, server.controller

state.path = None
state.user = None
state.badges = [
    'https://img.shields.io/circleci/build/github/girder/girder_web_components/master?style=for-the-badge',
    'https://img.shields.io/npm/v/@girder/components?style=for-the-badge',
    'https://img.shields.io/npm/dm/@girder/components?style=for-the-badge',
    'https://img.shields.io/bundlephobia/min/@girder/components?style=for-the-badge',
    'https://img.shields.io/github/stars/girder/girder_web_components?style=for-the-badge',
    ]
state.api_root = os.environ.get('VUE_APP_API_ROOT', 'http://localhost:8080/api/v1')

def disconnect():
    state.api_root = None
    state.path = None

def connect():
    state.api_root = state.path

@state.change('user')
def set_name(user, **kwargs):
    state.firstName = user.get('firstName', '').capitalize() if user else None
    state.lastName = user.get('lastName', '').upper() if user else None
    state.location = user if user else None

@state.change('location')
def upload_dest(location, **kwargs):
      if location and location.get('_modelType') == 'folder':
        state.upload_dest = location
      else:
        state.upload_dest = None

@state.change('location')
def data_details(location, **kwargs):
    if location and location.get('_id', ''):
        state.data_details = [location]
    else:
        state.data_details = []

def handle_search_select(item):
    if 'user' in item or 'folder' in item:
        state.location = item
    else:
        state.location = { '_modelType': 'folder', '_id': item.folderId }


# UI
with VAppLayout(server) as layout:
    with vuetify.VContainer():
        html.Div('Girder Web Components for Trame',
                 classes='display-3')
        with html.Div(classes='title mb-1'):
            html.Span('A Vue + Vuetify library for interacting with')
            html.A('data.kitware.com', href='https://data.kitware.com', target="_blank")
            html.Span('data management platform,')
            html.A('Girder', href='https://girder.readthedocs.io/en/stable/', target="_blank")

        html.Img(v_for='badge, i in badges',
                 key='i',
                 src='badge',
                 classes='pr-3')
        with vuetify.VRow():
            with vuetify.VCol(cols=10):
                with html.Div(classes='title mb-1'):
                    html.Span('This demo integrates with '),
                    html.A('data.kitware.com', href='https://data.kitware.com', target="_blank")
            with vuetify.VCol(cols=2, align="end"):
                vuetify.VSwitch(
                    v_model='$vuetify.theme.dark',
                    classes='mx-4 my-0',
                    hide_details='hide-details',
                    label='Dark theme',
                )

    with vuetify.VContainer(v_if=('!api_root',)):
        vuetify.VTextField(
            v_model=('path',),
            label='Girder API Root',
            filled=True,
            clearable=True,
        )

    with vuetify.VContainer(v_if=('api_root',)):
        with vuetify.VRow():
            with vuetify.VCol(cols=10):
                html.Div('Connected to ' + '{{ api_root }}')
            with vuetify.VCol(cols=2):
                vuetify.VBtn(
                    'Disconnect',
                    click=disconnect,
                    block=True,
                )

    with gwc.GirderProvider(v_if=('api_root',)) as provider:
        # AUTHENTICATION
        with vuetify.VContainer(v_if = ('!user',)):
            Headline(
                title='girder-authentication',
                link='src/components/Authentication/Authentication.vue',
                description='allows users to authenticate with girder',
            )
            gwc.GirderAuthentication(register=True)

        with vuetify.VContainer(v_else=True):
            with vuetify.VRow():
                with vuetify.VCol(cols=10):
                    html.Div('Welcome {} {}'.format(
                        '{{ firstName }} ', '{{ lastName }} '))
                with vuetify.VCol(cols=2):
                    vuetify.VBtn(
                        'Log Out',
                        click=provider.logout,
                        block=True
                    )

        # UPLOAD           
            Headline(
                title='girder-upload',
                link='src/components/Upload.vue',
                description='upload files to a specified location in girder',
            )
            gwc.GirderUpload(dest=('upload_dest', ))
            # TODO : when upload_dest is undefined write message

        # SEARCH
            # with vuetify.VCol(cols=12):
            #     html.Div('Search', classes='headline font-weight-bold mono mt-8')
            # with vuetify.VCol(cols=12):
            #     gwc.GirderSearch(v_on='select',
            #                      select='handle_search_select')

        # FILEMANAGER
            with vuetify.VRow():
                with vuetify.VCol(cols=7):
                    Headline(
                        title='girder-file-manager',
                        link='src/components/snippets/FileManager.vue',
                        description='a wrapper around girder-data-browser. \
                            It packages the browser with defaults including folder creation, \
                            item upload, and a breadcrumb bar',
                    )
                with vuetify.VCol(cols=5):
                    Headline(
                        title='girder-data-details',
                        link='src/components/DataDetails.vue',
                        description='in-depth information and controls for a single \
                            folder or item, or batch operations for groups of objects',
                    )
            with vuetify.VRow():
                with vuetify.VCol(cols=7):
                    gwc.GirderFileManager(root_location_disabled=False)
                with vuetify.VCol(cols=5):
                    gwc.GirderDataDetails(value=('data_details',))

        # JOB LIST
            Headline(
                title='girder-job-list',
                link='src/components/Job/JobList.vue',
                description='display and filter girder jobs',
            )
            gwc.GirderJobList()
        
        # ACCESS CONTROL
            Headline(
                title='girder-access-control',
                link='src/components/AccessControl.vue',
                description='access controls for folders and items',
            )
            gwc.GirderAccessControl(model=('upload_dest', ))
            
            # TODO : when upload_dest is undefined write message

            Headline(
                title='girder-upsert-folder',
                link='src/components/UpsertFolder.vue',
                description='create and edit folders',
            )
            # TODO Add switch Edit mode
            gwc.GirderUpsertFolder(location=('upload_dest', ))
            
            # TODO : when upload_dest is undefined write message
        
        # BREADCRUMB
            Headline(
                title='girder-breadcrumb',
                link='src/components/Breadcrumb.vue',
                description='filesystem path breadcrumb',
            )
            gwc.GirderBreadcrumb(location=('upload_dest', ))
            
            # TODO : when upload_dest is undefined write message


# Start the server
if __name__ == '__main__':
    server.start(port=12345)