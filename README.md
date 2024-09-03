# st_cookie 
## What 
`st_cookie` is a Python package that allows you to store and retrieve data in a cookie. 

## Installation
```bash
pip install st-cookie
```

## Usage
```python
import streamlit as st
from st_cookie import cookie_manager

# sync all you set by st_cookie from cookies to session state
# This can be use at the beginning of the script
cookie_manager.load_to_session_state()

# track a variable from st.session_state to cookies
with cookie_manager.record('my_textinput'):
    st.text_input("Enter text", key="my_textinput")

# or you can use it at on_change or on_click
st.checkbox("enabled", key="my_checkbox", on_change=lambda :cookie_manager.sync('my_checkbox'))


# (Not recommended) set a variable to cookies manually
# cookie_manager.set('my_variable', 'value')

# Get a variable from cookies
cookie_manager.get("my_textinput")
cookie_manager.get("my_checkbox")
```