from trame_client.utils.version import get_version

__version__ = get_version("trame-gwc")

AUTHENTICATION_KEYS = [
    "register",
    "oauth",
    "forgot_password_url",
    "forgot_password_route",
    "force_otp",
    "hide_forgot_password",
]
