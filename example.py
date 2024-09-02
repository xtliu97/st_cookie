import streamlit as st

from st_cookie import cookie_manager

cookie_manager.load_to_session_state()

st.write("Key in cookie, will load only on page refresh")
st.code(cookie_manager.get("test_cookie_key"))

st.write("Key in session state, will load on page refresh")
with cookie_manager.record("test_cookie_key"):
    st.text_input("Enter text", key="test_cookie_key")
st.code(st.session_state.get("test_cookie_key", ""))

