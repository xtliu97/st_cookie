# st-cookie

## What

`st-cookie` is a Python package that allows you to store and retrieve data in a cookie.

## Installation

```bash
pip install st-cookie
```

## Usage  

See `demo.py` for a brief example.v

### import

```python
import streamlit as st
import st_cookie
```

### Usage 1 (Recommend)  

Use context manager `st_cookie.sync()` to sync variables to between cookies and session states.

```python
with st_cookie.sync("my_textinput", "my_number"):
    st.text_input("Enter text", key="my_textinput")
    st.number_input("Enter number", key="my_number")
```

### Usage 2  

Use `st_cookie.apply()` to load all the variables from cookies to session state. Use `st_cookie.update` to update session states to cookies with `on_change` or `on_click` callback of streamlit components.

```python
st_cookie.apply()

st.checkbox(
    "enabled",
    key="my_checkbox",
    on_change=lambda: st_cookie.update("my_checkbox"),
)
```
