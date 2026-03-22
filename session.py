import streamlit as st

def set_session(username):
    """Set user session after successful login."""
    st.session_state['logged_in'] = True
    st.session_state['username'] = username

def clear_session():
    """Clear user session on logout."""
    st.session_state['logged_in'] = False
    st.session_state.pop('username', None)

def is_logged_in():
    """Check if user is currently logged in."""
    return st.session_state.get('logged_in', False)

def get_username():
    """Get current logged-in username."""
    if is_logged_in():
        return st.session_state.get('username')
    return None

def get_session():
    """Get session dictionary with user info."""
    if is_logged_in():
        return {
            'logged_in': True,
            'username': st.session_state.get('username')
        }
    return {'logged_in': False, 'username': None}
