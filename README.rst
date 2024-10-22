Girder Web Components for trame
==================================

trame-gwc extend trame **widgets** with components that can be used to authenticate to girder or to manage files.
It leverages [girder_web_components](https://github.com/girder/girder_web_components).


Installing
-----------------------------------------------------------

trame-gwc can be installed with **put pypi url**:

.. code-block:: bash

    pip install --upgrade trame-gwc


Usage
-----------------------------------------------------------

The `Trame Tutorial <https://kitware.github.io/trame/docs/tutorial.html>`_ is the place to go to learn how to use the library and start building your own application.

The `API Reference <https://trame.readthedocs.io/en/latest/index.html>`_ documentation provides API-level documentation.


License
-----------------------------------------------------------

trame-gwc is made available under the **precise license type** License.

Community
-----------------------------------------------------------

`Trame <https://kitware.github.io/trame/>`_ | `Discussions <https://github.com/Kitware/trame/discussions>`_ | `Issues <https://github.com/Kitware/trame/issues>`_ | `RoadMap <https://github.com/Kitware/trame/projects/1>`_ | `Contact Us <https://www.kitware.com/contact-us/>`_

.. image:: https://zenodo.org/badge/410108340.svg
    :target: https://zenodo.org/badge/latestdoi/410108340


Enjoying trame?
-----------------------------------------------------------

Share your experience `with a testimonial <https://github.com/Kitware/trame/issues/18>`_ or `with a brand approval <https://github.com/Kitware/trame/issues/19>`_.


Development: Grabbing client before push to PyPI
-----------------------------------------------------------

To update the client code, run the following command line while updating the targeted version

.. code-block:: console

    mkdir -p ./trame_gwc/module/serve
    curl https://unpkg.com/@girder/components -Lo ./trame_gwc/module/serve/girder_web_components.js

Simple example
-----------------------------------------------------------

.. code-block:: python
    from trame.app import get_server
    from trame.ui.vuetify import SinglePageLayout
    from trame.widgets import gwc
    from trame.widgets import vuetify2 as vuetify
    import os

    # Initialize server
    server = get_server(client_type = "vue2")
    state, ctrl = server.state, server.controller

    api_root = os.environ.get("VUE_APP_API_ROOT", "http://localhost:8080/api/v1")

    # UI
    with SinglePageLayout(server) as layout:
        layout.title.set_text("Girder Web Components for Trame")
        layout.toolbar.height = 50
        with layout.content:
            with vuetify.VContainer(classes="fill-height pa-0"):
                with vuetify.VRow(), vuetify.VCol(align_self="center"):
                    with gwc.GirderProvider(
                        api_root = api_root,
                    ):
                        gwc.GirderAuthentication(
                            register=True
                        )


    # Start the server
    if __name__ == "__main__":
        server.start(port=12345)
