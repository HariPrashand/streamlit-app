import streamlit as st
from auth import login_user
from session import clear_session

def login_page():
    st.title("🔐 Login")
    
    # Redirect if already logged in
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.switch_page("pages/patient_details.py")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("Enter your credentials to access your account")
        
        with st.form(key='login_form'):
            email = st.text_input(
                "Email",
                placeholder="your.email@example.com",
                help="Enter your registered email address"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                help="Enter your account password"
            )
            submit_button = st.form_submit_button("🔓 Login", use_container_width=True)
        
        if submit_button:
            # Validate inputs
            if not email or not password:
                st.error("⚠️ Please enter both email and password.")
            else:
                # Attempt login
                success, message = login_user(email, password)
                
                if success:
                    st.success("✅ " + message)
                    st.balloons()
                    st.switch_page("pages/patient_details.py")
                else:
                    st.error(f"❌ {message}")
        
        st.divider()
        st.write("Don't have an account? [Sign up here](signup)")

if __name__ == "__main__":
    login_page()
