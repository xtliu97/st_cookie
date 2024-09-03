__version__ = "0.1.2"

from ._cookie_manager import CookieManager

cookie_manager = CookieManager()
__all__ = ["cookie_manager"]
