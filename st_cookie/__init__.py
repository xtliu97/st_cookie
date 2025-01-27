from ._core import CookieManager


def apply():
    CookieManager().apply()


def update(key: str):
    CookieManager().update(key)


def sync(*keys: str):
    return CookieManager().sync(*keys)


def remove(key: str):
    CookieManager().remove(key)


def remove_all():
    CookieManager().remove_all()


def get_all():
    return CookieManager().get_all()


__all__ = ["apply", "update", "sync", "remove", "remove_all", "get_all"]
