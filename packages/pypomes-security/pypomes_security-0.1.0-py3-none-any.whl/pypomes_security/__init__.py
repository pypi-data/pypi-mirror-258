from .access_pomes import (
    SECURITY_TAG_USER_ID, SECURITY_TAG_USER_PWD,
    SECURITY_URL_GET_TOKEN, SECURITY_USER_ID, SECURITY_USER_PWD,
    access_get_token,
)

__all__ = [
    # access_pomes
    "SECURITY_TAG_USER_ID", "SECURITY_TAG_USER_PWD",
    "SECURITY_URL_GET_TOKEN", "SECURITY_USER_ID", "SECURITY_USER_PWD",
    "access_get_token",
]

from importlib.metadata import version
__version__ = version("pypomes_security")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
