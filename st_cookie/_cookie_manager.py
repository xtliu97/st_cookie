from contextlib import contextmanager
from typing import Any

import streamlit as st
from streamlit_cookies_controller import CookieController

from .core import CookieKV, _Key, key_prefix


class CookieManager:
    def __init__(self) -> None:
        self.cookie_controller = CookieController()

    def get(self, key: str) -> Any:
        if str_value := st.context.cookies.get(_Key(key).cookie_key):
            cookie_kv = CookieKV(key, str_value)
            return cookie_kv.value.raw
        return None

    def set(self, key: str, value: Any) -> None:
        cookie_kv = CookieKV(key, value)
        with st.container(height=1, border=False):
            st.html("<style>div[height='1']{display:none;}</style>")
            self.cookie_controller.set(cookie_kv.cookie_key, cookie_kv.value.to_str())

    def _is_session_start(self) -> bool:
        if "_is_session_start" in st.session_state:
            return False
        else:
            st.session_state["_is_session_start"] = True
            return True

    def get_all(self):
        with st.container(height=1, border=False):
            st.html("<style>div[height='1']{display:none;}</style>")
            return self.cookie_controller.getAll()

    def load_to_session_state(self) -> None:
        if not self._is_session_start():
            return

        for key in st.context.cookies.keys():
            if key.startswith(key_prefix):
                cookie_kv = CookieKV.from_str(key, st.context.cookies.get(key))
                st.session_state[cookie_kv.key] = cookie_kv.value.raw

    def remove_all(self) -> None:
        for key in st.context.cookies.keys():
            if key.startswith(key_prefix):
                self.remove(key)

    def remove(self, key: str) -> None:
        if key in self.cookie_controller.getAll():
            with st.container(height=1, border=False):
                st.html("<style>div[height='1']{display:none;}</style>")
                self.cookie_controller.remove(key)

    def sync(self, key: str) -> None:
        self.set(key, st.session_state[key])

    @contextmanager
    def record(self, key: str):
        yield
        self.set(key, st.session_state[key])
