__version__ = "0.1.3"

from ._cookie_manager import CookieManager

cookie_manager = CookieManager()
__all__ = ["cookie_manager"]
