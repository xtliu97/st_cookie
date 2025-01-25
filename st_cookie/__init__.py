from contextlib import contextmanager
from streamlit_cookies_controller import CookieController
from typing import List, Any
import streamlit as st
import logging

PREFIX = "st-cookie-"

ct = None


def get_cookie_controller():
    global ct
    if ct is None:
        ct = CookieController()
    return ct


def get_all():
    return get_cookie_controller().getAll()


def cookie_key_name(key: str) -> str:
    return f"{PREFIX}{key}"


def cookie_key_loaded(key: str) -> bool:
    k = f"{cookie_key_name(key)}-loaded"
    return k in st.session_state


def __cookie_to_session_state(key: str):
    if not cookie_key_loaded(key):
        cookie_key = cookie_key_name(key)
        st.session_state[key] = get_cookie_controller().get(cookie_key)
        st.session_state[f"{cookie_key}-loaded"] = True
        logging.debug(f"Loaded {key}: {st.session_state.get(key)}")


def _load_to_session_state(*keys: List[str]):
    logging.debug("Loading cookies to session state")
    exits_keys = list(get_cookie_controller().getAll().keys())
    for key in keys:
        if cookie_key_name(key) in exits_keys:
            __cookie_to_session_state(key)


def _save_to_cookie(key: str, value: Any):
    cookie_key = cookie_key_name(key)
    logging.debug(f"Saving {key}: {value}")
    with st.container(height=1, border=False):
        st.html("<style>div[height='1']{display:none;}</style>")
        get_cookie_controller().set(cookie_key, value)
        logging.debug(f"Saved {key}: {value}")


def apply():
    exits_keys = list(get_cookie_controller().getAll().keys())
    for key in exits_keys:
        if key.startswith(PREFIX):
            __cookie_to_session_state(key[len(PREFIX) :])


def update(key: str):
    _save_to_cookie(key, st.session_state[key])


@contextmanager
def sync(*keys: str):
    _load_to_session_state(*keys)
    yield
    for key in keys:
        _save_to_cookie(key, st.session_state[key])


def remove_all():
    exits_keys = list(get_cookie_controller().getAll().keys())
    for key in exits_keys:
        if key.startswith(PREFIX):
            get_cookie_controller().remove(key)
            logging.debug(f"Removed {key}")
