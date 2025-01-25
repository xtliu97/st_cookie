import streamlit as st
import st_cookie

st.set_page_config(layout="wide")


def display_session_state(key: str):
    st.write(f"{key}: {st.session_state.get(key)}")


def display_code(fn):
    import inspect

    code = inspect.getsource(fn)
    st.code(code, language="python")


def usage1():
    st_cookie.apply()

    st.checkbox(
        "Cached checkbox",
        key="my_checkbox",
        on_change=lambda: st_cookie.update("my_checkbox"),
    )
    display_session_state("my_checkbox")


def usage2():
    with st_cookie.sync("my_textinput", "my_number"):
        st.text_input("Enter text", key="my_textinput")
        st.number_input("Enter number", key="my_number")
        display_session_state("my_textinput")
        display_session_state("my_number")


def cookies_states():
    if st.button("Clear all", type="secondary"):
        st_cookie.remove_all()
    st.info(
        "All the related cookies values will be loaded only once after a new session is started."
    )
    with st.expander("Show all cookies", expanded=True):
        st.json(st_cookie.get_all())
        st.write(st.context.cookies)


def main():
    st.subheader("st-cookie", divider="gray")

    st.write("### Demo")
    usage1_col, usage2_col = st.columns(2)
    with usage1_col.container(height=600, border=True):
        st.write("#### Usage 1")
        display_code(usage1)
        usage1()

    with usage2_col.container(height=600, border=True):
        st.write("#### Usage 2")
        display_code(usage2)
        usage2()

    st.write("### Cookies states")
    cookies_states()


if __name__ == "__main__":
    main()
