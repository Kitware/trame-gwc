from pathlib import Path


serve_path = str(Path(__file__).with_name("serve").resolve())
serve = {"__trame_gwc": serve_path}
scripts = ["__trame_gwc/trame_gwc.umd.js"]
styles = ["__trame_gwc/trame_gwc.css"]
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
