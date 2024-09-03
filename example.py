import streamlit as st

from st_cookie import cookie_manager

st.set_page_config(layout="wide")

# sync all you set by st_cookie from cookies to session state
# This can be use at the beginning of the script
cookie_manager.load_to_session_state()

cookies_col, input_col, session_col = st.columns(3)

with cookies_col:
    st.write("### Cookies")
    st.write(
        "All cookies values will be load only once after the page is refreshed and will not be updated in one session."
    )
    st.write(cookie_manager.get_all())

    if st.button("Remove all"):
        cookie_manager.remove_all()

with input_col:
    st.write("### Inputs")

    # track a variable from st.session_state to cookies
    with cookie_manager.record("my_textinput", "my_number"):
        st.text_input("Enter text", key="my_textinput")
        st.number_input("Enter number", key="my_number")

    # or you can use it at on_change or on_click
    st.checkbox(
        "enabled",
        key="my_checkbox",
        on_change=lambda: cookie_manager.sync("my_checkbox"),
    )

    # (Not recommended) set a variable to cookies manually
    # cookie_manager.set("my_variable", "value")

with session_col:
    st.write("### Session State")
    st.write("All session state values will be updated immediately.")
    st.write("my_textinput", st.session_state.get("my_textinput"))
    st.write("my_number", st.session_state.get("my_number"))
    st.write("my_checkbox", st.session_state.get("my_checkbox"))
