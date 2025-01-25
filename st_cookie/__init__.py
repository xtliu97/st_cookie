__version__ = "0.2.3"

from ._cookie_manager import CookieManager


def get_manager():
    return CookieManager()


__all__ = ["get_manager"]
