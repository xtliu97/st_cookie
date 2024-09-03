import base64
import pickle
from typing import Any, Generic, TypeVar
from urllib.parse import unquote

key_prefix = "st_cookie__"


class _Key:
    def __init__(self, key: str, key_prefix: str = key_prefix):
        self.__key_prefix = key_prefix
        self.__key = key.removeprefix(self.__key_prefix)

    @property
    def cookie_key(self) -> str:
        return f"{self.__key_prefix}{self.__key}"

    @property
    def raw(self) -> str:
        return self.__key


def obj_to_txt(obj: Any):
    # Serialize an object into a plain text
    message_bytes = pickle.dumps(obj)
    base64_bytes = base64.b64encode(message_bytes)
    txt = base64_bytes.decode("ascii")
    return txt


# De-serialize an object from a plain text
def txt_to_obj(txt: str) -> Any:
    txt = unquote(txt)
    base64_bytes = txt.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    obj = pickle.loads(message_bytes)
    return obj


T = TypeVar("T")


class _Value(Generic[T]):
    def __init__(self, value: T):
        if isinstance(value, _Value):
            value = value.raw
        self.__value = value

    @property
    def raw(self) -> T:
        return self.__value

    @classmethod
    def from_str(cls, value: str):
        return _Value(txt_to_obj(value))

    def to_str(self) -> str:
        return obj_to_txt(self.__value)


class CookieKV(Generic[T]):
    def __init__(self, key: str, value: T):
        self.__key = _Key(key)
        self.__value = _Value(value)

    @property
    def key(self) -> str:
        return self.__key.raw

    @property
    def cookie_key(self) -> str:
        return self.__key.cookie_key

    @property
    def value(self) -> _Value[T]:
        return self.__value

    @classmethod
    def from_str(cls, key: str, value: str):
        return cls(key, _Value.from_str(value))

    def __str__(self) -> str:
        return f"{self.cookie_key}: {self.value.raw}"
