from contextlib import contextmanager
from typing import Any
from urllib.parse import unquote

import streamlit as st
from streamlit_cookies_controller import CookieController

from .core import CookieKV, key_prefix


class CookieManager:
    def __init__(self) -> None:
        self.cookie_controller = CookieController()

    def get(self, key: str) -> Any:
        str_value = st.context.cookies.get(key)
        if str_value is None:
            return None
        return CookieKV.from_str(key, str_value).value

    def set(self, key: str, value: Any) -> None:
        cookie_kv = CookieKV(key, value)
        self.cookie_controller.set(cookie_kv.cookie_key, cookie_kv.value.to_str())

    def _is_session_start(self) -> bool:
        if "_is_session_start" in st.session_state:
            return False
        else:
            st.session_state["_is_session_start"] = True
            return True

    def load_to_session_state(self) -> None:
        if not self._is_session_start():
            return

        for key in st.context.cookies.keys():
            if key.startswith(key_prefix):
                unquoted_value = unquote(st.context.cookies.get(key))
                cookie_kv = CookieKV.from_str(key, unquoted_value)
                st.session_state[cookie_kv.key] = cookie_kv.value.raw

    def remove_all(self) -> None:
        for key in st.context.cookies.keys():
            if key.startswith(key_prefix):
                self.remove(key)

    def remove(self, key: str) -> None:
        self.cookie_controller.remove(key)

    def update(self, key: str) -> None:
        self.set(key, st.session_state[key])

    @contextmanager
    def sync(self, key: str):
        yield
        self.set(key, st.session_state[key])
