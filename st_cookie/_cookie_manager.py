import threading
import time
from contextlib import contextmanager
from typing import Any, Dict, List, Literal, Optional

import streamlit as st
from streamlit_cookies_controller import CookieController

from .core import CookieKV, SerializationError, _Key, key_prefix


class CookieError(Exception):
    """Base exception for cookie-related errors."""

    pass


class Singleton(type):
    """Thread-safe implementation of the Singleton pattern."""

    _instances: Dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking pattern
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class CookieManager(metaclass=Singleton):
    """
    Manages cookie operations in a Streamlit application.
    Thread-safe singleton implementation ensures only one instance exists.
    """

    def __init__(self) -> None:
        self.cookie_controller = CookieController()
        self._lock = threading.Lock()

    def _get(self, key: str) -> Optional[CookieKV]:
        """
        Internal method to get a cookie value.

        Args:
            key: Cookie key

        Returns:
            Optional[CookieKV]: Cookie key-value pair if exists, None otherwise

        Raises:
            CookieError: If cookie value cannot be deserialized
        """
        try:
            if str_value := st.context.cookies.get(_Key(key).cookie_key):
                return CookieKV.from_str(key, str_value)
        except (ValueError, SerializationError) as e:
            raise CookieError(f"Failed to get cookie '{key}': {str(e)}")
        return None

    def get(self, key: str) -> Any:
        """
        Get a cookie value.

        Args:
            key: Cookie key

        Returns:
            Any: Cookie value if exists, None otherwise

        Raises:
            CookieError: If cookie value cannot be retrieved
        """
        try:
            cookie_kv = self._get(key)
            return cookie_kv.value.raw if cookie_kv else None
        except Exception as e:
            raise CookieError(f"Failed to get cookie '{key}': {str(e)}")

    def set(self, key: str, value: Any) -> None:
        """
        Set a cookie value.

        Args:
            key: Cookie key
            value: Cookie value (must be JSON serializable)

        Raises:
            CookieError: If cookie value cannot be set
        """
        try:
            cookie_kv = CookieKV(key, value)
            with st.container(height=1, border=False):
                st.html("<style>div[height='1']{display:none;}</style>")
                self.cookie_controller.set(
                    cookie_kv.cookie_key, cookie_kv.value.to_str()
                )
        except Exception as e:
            raise CookieError(f"Failed to set cookie '{key}': {str(e)}")

    def _is_session_start(self) -> bool:
        """Check if this is the start of a new session."""
        with self._lock:
            if "_is_session_start" in st.session_state:
                return False
            st.session_state["_is_session_start"] = True
            return True

    def get_all(
        self, backend: Literal["streamlit", "cookie_controller"] = "streamlit"
    ) -> Dict[str, Any]:
        """
        Get all cookies.

        Args:
            backend: Backend to use for getting cookies

        Returns:
            Dict[str, Any]: Dictionary of cookie key-value pairs

        Raises:
            CookieError: If cookies cannot be retrieved
            ValueError: If invalid backend specified
        """
        try:
            all_cookies = {}
            if backend == "streamlit":
                all_cookie_keys = st.context.cookies.keys()
            elif backend == "cookie_controller":
                all_cookie_keys = self.cookie_controller.getAll().keys()
                time.sleep(0.1)  # Reduced sleep time
            else:
                raise ValueError(f"Invalid backend: {backend}")

            for key in all_cookie_keys:
                if key.startswith(key_prefix):
                    try:
                        cookie_kv = CookieKV.from_str(key, st.context.cookies.get(key))
                        all_cookies[cookie_kv.key] = cookie_kv.value.raw
                    except (ValueError, SerializationError) as e:
                        st.warning(f"Skipping invalid cookie '{key}': {str(e)}")
            return all_cookies
        except Exception as e:
            raise CookieError(f"Failed to get all cookies: {str(e)}")

    def load_to_session_state(
        self, keeps: List[str] = None, ignores: List[str] = None
    ) -> None:
        """
        Load cookies to session state.

        Args:
            keeps: List of keys to keep (if None, keep all)
            ignores: List of keys to ignore

        Raises:
            CookieError: If cookies cannot be loaded to session state
        """
        try:
            target_keys = (
                [_Key(key).cookie_key for key in keeps]
                if keeps
                else st.context.cookies.keys()
            )
            ignores = set(_Key(key).cookie_key for key in ignores) if ignores else set()

            for key in target_keys:
                if key.startswith(key_prefix) and key not in ignores:
                    self.__cookie_to_session_state(key)
        except Exception as e:
            raise CookieError(f"Failed to load cookies to session state: {str(e)}")

    def __cookie_to_session_state(self, key: str):
        """Load a single cookie to session state."""
        _cookie_key_loaded = f"{key_prefix}{key}_cookie_loaded"

        if _cookie_key_loaded in st.session_state:
            return

        try:
            if cookie_kv := self._get(key):
                st.session_state[cookie_kv.key] = cookie_kv.value.raw
            st.session_state[_cookie_key_loaded] = True
        except Exception as e:
            st.warning(f"Failed to load cookie '{key}' to session state: {str(e)}")

    def remove_all(self) -> None:
        """Remove all cookies."""
        try:
            for key in st.context.cookies.keys():
                if key.startswith(key_prefix):
                    self.remove(key)
            st.rerun()
        except Exception as e:
            raise CookieError(f"Failed to remove all cookies: {str(e)}")

    def remove(self, key: str) -> None:
        """
        Remove a cookie.

        Args:
            key: Cookie key to remove

        Raises:
            CookieError: If cookie cannot be removed
        """
        try:
            if key in self.cookie_controller.getAll():
                with st.container(height=1, border=False):
                    st.html("<style>div[height='1']{display:none;}</style>")
                    self.cookie_controller.remove(key)
        except Exception as e:
            raise CookieError(f"Failed to remove cookie '{key}': {str(e)}")

    def update(self, key: str) -> None:
        self.set(key, st.session_state[key])

    @contextmanager
    def sync(self, *keys: str):
        self.load_to_session_state(*keys)
        yield
        for key in keys:
            self.set(key, st.session_state[key])
