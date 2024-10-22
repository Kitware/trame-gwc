from trame.widgets import html
from trame.widgets import vuetify2 as vuetify

repo_base = 'https://github.com/girder/girder_web_components/blob/master/'

def Headline(title, description, link):
    with html.Div():
        with html.Div(title, classes="headline font-weight-bold mono mt-8"):
            with vuetify.VBtn(href=repo_base + link, icon="icon", classes="ml-2", title="View Source"):
                vuetify.VIcon("mdi-open-in-new")
        html.Div(description, classes="subtitle-1 mb-4")

def NavLink():
    pass