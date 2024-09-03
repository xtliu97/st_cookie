import streamlit as st

from st_cookie import cookie_manager

if st.button("Clear all cookies"):
    cookie_manager.remove_all()

cookie_manager.load_to_session_state()

st.write("Key in cookie, will load only on page refresh")
st.code(cookie_manager.get("test_cookie_key"))

st.write("Key in session state, will load on page refresh")
with cookie_manager.sync("test_cookie_key"):
    a = st.checkbox("Enter text", key="test_cookie_key")
st.code(st.session_state.get("test_cookie_key", ""))

st.json(st.context.cookies)
