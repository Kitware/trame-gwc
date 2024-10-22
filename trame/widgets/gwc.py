from trame_gwc.widgets.gwc import *


def initialize(server):
    from trame_gwc import module

    server.enable_module(module)