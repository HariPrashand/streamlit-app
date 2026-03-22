import bcrypt
import re
from db import users_collection
from session import set_session

def hash_password(password):
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    """Verify password against hashed password."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception:
        return False

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength (min 6 chars, at least 1 uppercase, 1 lowercase, 1 digit)."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    return True, "Valid"

def validate_username(username):
    """Validate username format (3-20 chars, alphanumeric and underscore only)."""
    if not username or len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, "Valid"

def signup_user(email, password, username):
    """Create new user account with validation."""
    # Validate inputs
    if not email or not password or not username:
        return False, "All fields are required."
    
    if not validate_email(email):
        return False, "Invalid email format."
    
    is_valid_password, message = validate_password(password)
    if not is_valid_password:
        return False, message
    
    is_valid_username, message = validate_username(username)
    if not is_valid_username:
        return False, message
    
    # Check if email already exists
    if users_collection.find_one({"email": email}):
        return False, "Email already registered."
    
    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return False, "Username already taken."
    
    # Create new user
    try:
        hashed_password = hash_password(password)
        users_collection.insert_one({
            "email": email,
            "password": hashed_password,
            "username": username
        })
        return True, "Account created successfully."
    except Exception as e:
        return False, f"Error creating account: {str(e)}"

def login_user(email, password):
    """Authenticate user with email and password."""
    if not email or not password:
        return False, "Email and password are required."
    
    try:
        user = users_collection.find_one({"email": email})
        if user and check_password(user['password'], password):
            set_session(user['username'])
            return True, "Login successful."
        return False, "Invalid email or password."
    except Exception as e:
        return False, f"Error during login: {str(e)}"
