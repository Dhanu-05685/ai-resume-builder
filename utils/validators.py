import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_upper and has_lower and has_digit

def validate_username(username):
    """Validate username format"""
    if len(username) < 3 or len(username) > 50:
        return False
    
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, username) is not None

def validate_filename(filename):
    """Validate file name"""
    if not filename or len(filename) > 255:
        return False
    
    # Allow only alphanumeric, dash, underscore, and dot
    pattern = r'^[a-zA-Z0-9_\-\.]+$'
    return re.match(pattern, filename) is not None

def sanitize_text(text):
    """Remove harmful characters from text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    return text.strip()

def validate_resume_name(name):
    """Validate resume name"""
    if not name or len(name) < 3 or len(name) > 100:
        return False
    return True
