from pathlib import Path

from trame_gwc import __version__

serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {f"__trame_gwc_{__version__}": serve_path}
scripts = [f"__trame_gwc_{__version__}/trame_gwc.umd.js"]
styles = [f"__trame_gwc_{__version__}/trame_gwc.css"]
vue_use = [
    (
        "trame_gwc",
        {
            "girder": {"apiRoot": None},
            "components": True,
        },
    )
]


def setup(server, **kwargs):
    client_type = "vue3"
    if hasattr(server, "client_type"):
        client_type = server.client_type

    if client_type != "vue3":
        msg = f"Server using client_type='{client_type}' while we expect 'vue3'"
        raise TypeError(msg)
