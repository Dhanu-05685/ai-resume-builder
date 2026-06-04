from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.validators import validate_email, validate_password
from database.db_helper import create_user, get_user_by_email, get_user_by_id

auth_bp = Blueprint('auth', __name__)

# ============ LOGIN ============

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return render_template('auth/login.html', error='Email and password required')
        
        user = get_user_by_email(email)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard.dashboard'))
        else:
            return render_template('auth/login.html', error='Invalid email or password')
    
    return render_template('auth/login.html')

# ============ SIGNUP ============

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            return render_template('auth/signup.html', error='All fields are required')
        
        if len(username) < 3:
            return render_template('auth/signup.html', error='Username must be at least 3 characters')
        
        if not validate_email(email):
            return render_template('auth/signup.html', error='Invalid email format')
        
        if not validate_password(password):
            return render_template('auth/signup.html', 
                                 error='Password must be at least 8 characters with uppercase, lowercase, and numbers')
        
        if password != confirm_password:
            return render_template('auth/signup.html', error='Passwords do not match')
        
        # Check if user exists
        existing_user = get_user_by_email(email)
        if existing_user:
            return render_template('auth/signup.html', error='Email already registered')
        
        # Create user
        hashed_password = generate_password_hash(password)
        user_id = create_user(username, email, hashed_password)
        
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('dashboard.dashboard'))
        else:
            return render_template('auth/signup.html', error='Error creating account')
    
    return render_template('auth/signup.html')

# ============ LOGOUT ============

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============ FORGOT PASSWORD (Optional) ============

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return render_template('auth/forgot_password.html', error='Email required')
        
        user = get_user_by_email(email)
        if user:
            # TODO: Send reset email
            return render_template('auth/forgot_password.html', 
                                 message='If email exists, password reset link has been sent')
        
        return render_template('auth/forgot_password.html', 
                             message='If email exists, password reset link has been sent')
    
    return render_template('auth/forgot_password.html')

# ============ API ENDPOINTS ============

@auth_bp.route('/api/check-email', methods=['POST'])
def check_email():
    email = request.json.get('email', '').strip()
    
    if not validate_email(email):
        return jsonify({'available': False, 'message': 'Invalid email'}), 400
    
    user = get_user_by_email(email)
    return jsonify({'available': user is None})

@auth_bp.route('/api/check-username', methods=['POST'])
def check_username():
    username = request.json.get('username', '').strip()
    
    if len(username) < 3:
        return jsonify({'available': False, 'message': 'Username too short'}), 400
    
    # Check if username exists (you need to implement this function)
    from database.db_helper import get_user_by_username
    user = get_user_by_username(username)
    return jsonify({'available': user is None})
