import streamlit as st
from st_cookie import get_manager

st.set_page_config(layout="wide")

cookie_manager = get_manager()


def usage1():
    cookie_manager.load_to_session_state()

    st.checkbox(
        "enabled",
        key="my_checkbox",
        on_change=lambda: cookie_manager.update("my_checkbox"),
    )

    st.write("my_checkbox", st.session_state.get("my_checkbox"))


def usage2():
    with cookie_manager.sync("my_textinput", "my_number"):
        st.text_input("Enter text", key="my_textinput")
        st.number_input("Enter number", key="my_number")

    st.write("my_textinput", st.session_state.get("my_textinput"))
    st.write("my_number", st.session_state.get("my_number"))


def st_code_fn(fn):
    import inspect

    code = inspect.getsource(fn)
    st.code(code, language="python")


def cookies_states():
    if st.button("Clear all", type="secondary"):
        cookie_manager.remove_all()
    st.info(
        "All the related cookies values will be loaded only once after a new session is started."
    )
    with st.expander("Show all cookies", expanded=True):
        st.json(cookie_manager.get_all())


def main():
    st.subheader("st-cookie", divider="gray")

    st.write("### Demo")
    usage1_col, usage2_col = st.columns(2)
    with usage1_col.container(height=600, border=True):
        st.write("#### Usage 1")
        st_code_fn(usage1)
        usage1()

    with usage2_col.container(height=600, border=True):
        st.write("#### Usage 2")
        st_code_fn(usage2)
        usage2()

    st.write("### Cookies states")
    cookies_states()


if __name__ == "__main__":
    main()
