
import urllib.parse
from contextlib import contextmanager
from typing import overload

import streamlit as st
from streamlit_cookies_controller import CookieController

__version__ = "0.1.0"
key_prefix = "st_cookie__"

class KeyName:    
    def __init__(self, key: str, key_prefix: str = key_prefix):
        self.__key_prefix = key_prefix
        self.__key = key.removeprefix(self.__key_prefix)
        
    @property
    def cookie_key(self) -> str:
        return f"{self.__key_prefix}{self.__key}"

    @property
    def raw_key(self) -> str:
        return self.__key

    @classmethod
    def is_cookie_key(cls, key:str, key_prefix:str = key_prefix) -> bool:
        return key.startswith(key_prefix)
 

class CookieManager:
    def __init__(self) -> None:
        self.cookie_controller = CookieController()

    def get(self, key: str, default: str = ""):
        """Get cookie value by key via st.context.cookies"""
        return urllib.parse.unquote(st.context.cookies.get(KeyName(key).cookie_key, default))

    def set(self, key: str, value: str):
        """Set cookie value by key via streamlit_cookies_controller"""
        self.cookie_controller.set(KeyName(key).cookie_key, value)

    def load_to_session_state(self):
        """Sync cookies to st.session_state"""
        __new_session_key = "__new_session_key"
        # only run when new session starts
        if __new_session_key in st.session_state:
            return
        st.session_state[__new_session_key] = True
        
        # sync session state to cookies
        for key in st.context.cookies.keys():
            if KeyName.is_cookie_key(key):
                st.session_state[KeyName(key).raw_key] = self.get(key)
        
        
    def __sync_impl(self, key:str | list[str]):
        if isinstance(key, str):
            key = [key]
        for k in key:
            self.set(k, st.session_state.get(k, ""))
                
    @contextmanager
    def record(self, *keys:str):
        yield
        print("record", keys)
        self.__sync_impl(keys)


cookie_manager = CookieManager()