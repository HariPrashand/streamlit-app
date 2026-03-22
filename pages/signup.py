import streamlit as st
from auth import signup_user, validate_email, validate_password, validate_username
from session import set_session
from time import sleep

def signup_page():
    st.title("📝 Sign Up")
    
    # Redirect if already logged in
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.switch_page("pages/patient_details.py")
        return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("Create a new account to get started")
        
        with st.form(key='signup_form'):
            email = st.text_input(
                "Email",
                placeholder="your.email@example.com",
                help="Enter a valid email address"
            )
            
            username = st.text_input(
                "Username",
                placeholder="username123",
                help="3-20 characters, letters, numbers, and underscores only"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                help="Min 6 chars, must include uppercase, lowercase, and digit"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                help="Passwords must match"
            )
            
            submit_button = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if submit_button:
            # Validate inputs exist
            if not email or not username or not password or not confirm_password:
                st.error("⚠️ Please fill in all fields.")
            # Validate passwords match
            elif password != confirm_password:
                st.error("❌ Passwords do not match.")
            # Validate email format
            elif not validate_email(email):
                st.error("❌ Please enter a valid email address.")
            # Validate username format
            else:
                is_valid_username, username_message = validate_username(username)
                if not is_valid_username:
                    st.error(f"❌ {username_message}")
                else:
                    # Validate password strength
                    is_valid_password, password_message = validate_password(password)
                    if not is_valid_password:
                        st.error(f"❌ {password_message}")
                    else:
                        # Attempt signup
                        success, message = signup_user(email, password, username)
                        
                        if success:
                            st.success("✅ " + message)
                            set_session(username)
                            sleep(1)
                            st.switch_page("pages/patient_details.py")
                        else:
                            st.error(f"❌ {message}")
        
        # Password requirements info
        with st.expander("📋 Password Requirements"):
            st.markdown("""
            Your password must contain:
            - At least 6 characters
            - At least one uppercase letter (A-Z)
            - At least one lowercase letter (a-z)
            - At least one digit (0-9)
            """)
        
        st.divider()
        st.write("Already have an account? [Login here](login)")

if __name__ == "__main__":
    signup_page()
