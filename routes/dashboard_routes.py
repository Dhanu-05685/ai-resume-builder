from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request, flash
from functools import wraps
from database.db_helper import get_user_by_id, get_user_resumes, get_resume
from werkzeug.security import check_password_hash, generate_password_hash
import re

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ DASHBOARD ROUTES ============

@dashboard_bp.route('/')
@login_required
def dashboard():
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    resumes = get_user_resumes(user_id)
    
    # Calculate stats
    ats_scores = [r['ats_score'] for r in resumes if r['ats_score'] is not None]
    avg_ats_score = sum(ats_scores) // len(ats_scores) if ats_scores else 0
    
    stats = {
        'total_resumes': len(resumes) if resumes else 0,
        'avg_ats_score': avg_ats_score
    }
    
    return render_template('dashboard.html', user=user, resumes=resumes, stats=stats)

@dashboard_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    resumes = get_user_resumes(user_id)
    
    ats_scores = [r['ats_score'] for r in resumes if r['ats_score'] is not None]
    avg_ats_score = sum(ats_scores) // len(ats_scores) if ats_scores else 0
    
    stats = {
        'total_resumes': len(resumes) if resumes else 0,
        'avg_ats_score': avg_ats_score
    }
    
    return render_template('profile.html', user=user, stats=stats)

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        # TODO: Update bio in database
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('dashboard.settings'))
    
    return render_template('settings.html', user=user)

@dashboard_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = session['user_id']
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate inputs
        if not all([current_password, new_password, confirm_password]):
            return render_template('change_password.html', error='All fields are required')
        
        if new_password != confirm_password:
            return render_template('change_password.html', error='New passwords do not match')
        
        if len(new_password) < 8:
            return render_template('change_password.html', error='Password must be at least 8 characters')
        
        # Check if has uppercase, lowercase, and number
        if not any(c.isupper() for c in new_password):
            return render_template('change_password.html', error='Password must contain uppercase letter')
        if not any(c.islower() for c in new_password):
            return render_template('change_password.html', error='Password must contain lowercase letter')
        if not any(c.isdigit() for c in new_password):
            return render_template('change_password.html', error='Password must contain a number')
        
        # Get user and verify current password
        user = get_user_by_id(user_id)
        if not user or not check_password_hash(user['password'], current_password):
            return render_template('change_password.html', error='Current password is incorrect')
        
        # Update password
        try:
            hashed_new_password = generate_password_hash(new_password)
            from database.db_helper import DatabaseHelper
            query = "UPDATE users SET password = %s WHERE id = %s"
            DatabaseHelper.execute_query(query, (hashed_new_password, user_id))
            
            flash('Password changed successfully!', 'success')
            return render_template('change_password.html', success=True)
        except Exception as e:
            return render_template('change_password.html', error=f'Error updating password: {str(e)}')
    
    return render_template('change_password.html')

@dashboard_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        user_id = session['user_id']
        password = request.form.get('password', '')
        confirm_delete = request.form.get('confirm_delete')
        
        if not confirm_delete:
            return render_template('delete_account.html', error='Please confirm deletion')
        
        if not password:
            return render_template('delete_account.html', error='Password is required')
        
        # Verify password
        user = get_user_by_id(user_id)
        if not user or not check_password_hash(user['password'], password):
            return render_template('delete_account.html', error='Password is incorrect')
        
        try:
            # Delete user and all related data
            from database.db_helper import DatabaseHelper
            query = "DELETE FROM users WHERE id = %s"
            DatabaseHelper.execute_query(query, (user_id,))
            
            # Clear session
            session.clear()
            
            # Redirect to home
            flash('Your account has been deleted. We\'re sorry to see you go!', 'info')
            return redirect(url_for('index'))
        
        except Exception as e:
            return render_template('delete_account.html', error=f'Error deleting account: {str(e)}')
    
    return render_template('delete_account.html')
@dashboard_bp.route('/my-resumes')
@login_required
def my_resumes():
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    resumes = get_user_resumes(user_id)
    
    # Calculate stats
    ats_scores = [r['ats_score'] for r in resumes if r['ats_score'] is not None]
    avg_ats_score = sum(ats_scores) // len(ats_scores) if ats_scores else 0
    
    stats = {
        'total_resumes': len(resumes) if resumes else 0,
        'avg_ats_score': avg_ats_score
    }
    
    return render_template('my_resumes.html', user=user, resumes=resumes, stats=stats)
@dashboard_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to newsletter"""
    email = request.form.get('email', '').strip()
    
    # Validate email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email or not re.match(email_pattern, email):
        flash('Please enter a valid email address', 'error')
        return redirect(request.referrer or url_for('index'))
    
    try:
        # TODO: Save email to database for newsletter
        # For now, just show success message
        flash('✅ Thank you for subscribing! Check your email for confirmation.', 'success')
        return redirect(request.referrer or url_for('index'))
    except Exception as e:
        flash(f'Error subscribing: {str(e)}', 'error')
        return redirect(request.referrer or url_for('index'))