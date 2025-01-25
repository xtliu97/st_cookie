import base64
import json
from typing import Any, Generic, TypeVar
from urllib.parse import unquote

key_prefix = "st_cookie__"


class SerializationError(Exception):
    """Exception raised for errors during serialization/deserialization."""
    pass


class _Key:
    def __init__(self, key: str, key_prefix: str = key_prefix):
        if not isinstance(key, str):
            raise ValueError("Cookie key must be a string")
        self.__key_prefix = key_prefix
        self.__key = key.removeprefix(self.__key_prefix)

    @property
    def cookie_key(self) -> str:
        return f"{self.__key_prefix}{self.__key}"

    @property
    def raw(self) -> str:
        return self.__key


def obj_to_txt(obj: Any) -> str:
    """
    Serialize an object into a plain text using JSON.
    
    Args:
        obj: Any JSON-serializable object
        
    Returns:
        str: Base64 encoded JSON string
        
    Raises:
        SerializationError: If object cannot be serialized
    """
    try:
        json_str = json.dumps(obj)
        base64_bytes = base64.b64encode(json_str.encode('utf-8'))
        return base64_bytes.decode('ascii')
    except (TypeError, json.JSONDecodeError) as e:
        raise SerializationError(f"Failed to serialize object: {str(e)}")


def txt_to_obj(txt: str) -> Any:
    """
    De-serialize an object from a plain text using JSON.
    
    Args:
        txt: Base64 encoded JSON string
        
    Returns:
        Any: Deserialized object
        
    Raises:
        SerializationError: If text cannot be deserialized
    """
    try:
        txt = unquote(txt)
        base64_bytes = txt.encode('ascii')
        json_str = base64.b64decode(base64_bytes).decode('utf-8')
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError, base64.binascii.Error) as e:
        raise SerializationError(f"Failed to deserialize text: {str(e)}")


T = TypeVar('T')


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
        try:
            return _Value(txt_to_obj(value))
        except SerializationError as e:
            raise ValueError(f"Invalid cookie value: {str(e)}")

    def to_str(self) -> str:
        try:
            return obj_to_txt(self.__value)
        except SerializationError as e:
            raise ValueError(f"Invalid cookie value: {str(e)}")


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
