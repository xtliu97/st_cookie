# st_cookie 
## What 
`st_cookie` is a Python package that allows you to store and retrieve data in a cookie. 

## Installation
```bash
pip install st-cookie
```

## Usage
- import
```python
from st_cookie import cookie_manager
```

- Usage 1  
Use `cookie_manager.load_to_session_state()` to load all the variables from cookies to session state. Use `cookie_manager.update()` to update session states to cookies with `on_change` or `on_click` callback of streamlit components.
```python
cookie_manager.load_to_session_state()

st.checkbox(
    "enabled",
    key="my_checkbox",
    on_change=lambda: cookie_manager.update("my_checkbox"),
)
```

- Usage 2  
Use context manager `cookie_manager.sync()` to sync variables to between cookies and session states.
```python
with cookie_manager.sync("my_textinput", "my_number"):
    st.text_input("Enter text", key="my_textinput")
    st.number_input("Enter number", key="my_number")
```