from contextlib import contextmanager
from typing import Any, Dict, List

import streamlit as st
from streamlit_cookies_controller import CookieController

PREFIX = "st-cookie-"


class _Singleton(type):
    """A metaclass that creates a Singleton base class when called
    with the class keyword.
    """

    def __init__(cls, name, bases, dict):
        super(_Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class CookieManager(metaclass=_Singleton):
    """A class to manage cookies in Streamlit."""

    def __init__(self):
        self._cookie_controller = CookieController()

    @staticmethod
    def _cookie_key(key: str) -> str:
        return f"{PREFIX}{key}"

    @property
    def exist_keys(self) -> List[str]:
        return list(self.get_all().keys())

    def _cookie_key_loaded(self, key: str) -> bool:
        return f"{self._cookie_key(key)}-loaded" in st.session_state

    def _cookie_to_session_state(self, key: str):
        if not self._cookie_key_loaded(key):
            cookie_key = self._cookie_key(key)
            st.session_state[key] = self._cookie_controller.get(cookie_key)
            st.session_state[f"{cookie_key}-loaded"] = True

    def _save_to_cookie(self, key: str, value: Any):
        cookie_key = self._cookie_key(key)
        with st.container(height=1, border=False):
            st.html("<style>div[height='1']{display:none;}</style>")
            self._cookie_controller.set(cookie_key, value)

    def get_all(self) -> Dict[str, Any]:
        return self._cookie_controller.getAll()

    def apply(self) -> None:
        for key in self.exist_keys:
            if key.startswith(PREFIX):
                self._cookie_to_session_state(key[len(PREFIX) :])

    def _update(self, key: str, value: Any) -> None:
        self._save_to_cookie(key, value)

    def update(self, key: str) -> None:
        self._update(key, st.session_state[key])

    @contextmanager
    def sync(self, *keys: str):
        # Load cookies to session state
        for key in keys:
            if self._cookie_key(key) in self.exist_keys:
                self._cookie_to_session_state(key)

        yield

        # Save session state to cookies
        for key in keys:
            self._save_to_cookie(key, st.session_state[key])

    def remove(self, key: str) -> None:
        cookie_key = self._cookie_key(key)
        self._cookie_controller.remove(cookie_key)

    def remove_all(self) -> None:
        for key in self.exist_keys:
            if key.startswith(PREFIX):
                self._cookie_controller.remove(key)
