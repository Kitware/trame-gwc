from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_gwc": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_gwc/trame-gwc.umd.min.js"]

vue_use = ["trame_gwc"]

# List of CSS files to load (usually from the serve path above)
styles = ["__trame_gwc/trame-gwc.css"]