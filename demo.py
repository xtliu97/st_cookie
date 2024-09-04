import streamlit as st

from st_cookie import cookie_manager

st.set_page_config(layout="wide")

st.write("## st_cookie demo")
main_col, cookie_col = st.columns([4,1])

with cookie_col:
    st.write("### Cookies")
    if st.button("Clear all"):
        cookie_manager.remove_all()
    st.info("All the related cookies values will be loaded only once after a new session is started.")
    with st.expander("Show all cookies"):
        st.json(cookie_manager.get_all())


usage_code1 = r"""
cookie_manager.load_to_session_state()

st.checkbox(
    "enabled",
    key="my_checkbox",
    on_change=lambda: cookie_manager.update("my_checkbox"),
)

st.write("my_checkbox", st.session_state.get("my_checkbox"))
"""


usage_code2 = r"""
with cookie_manager.sync("my_textinput", "my_number"):
    st.text_input("Enter text", key="my_textinput")
    st.number_input("Enter number", key="my_number")
    
st.write("my_textinput", st.session_state.get("my_textinput"))
st.write("my_number", st.session_state.get("my_number"))
"""


usage1_col, usage2_col = main_col.columns(2)
with usage1_col.container(height=500, border=True):
    st.write("#### Usage 1")
    st.code(usage_code1, language="python")
    exec(usage_code1)
        
with usage2_col.container(height=500, border=True):
    st.write("#### Usage 2")
    st.code(usage_code2, language="python")
    exec(usage_code2)
