import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import mysql.connector

# Import routes
from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.dashboard_routes import dashboard_bp
from routes.cover_letter_routes import cover_letter_bp
from routes.interview_routes import interview_bp
# Import utilities
from utils.validators import validate_email, validate_password
from database.db_helper import DatabaseHelper

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(resume_bp, url_prefix='/resume')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(cover_letter_bp, url_prefix='/cover-letter')
app.register_blueprint(interview_bp, url_prefix='/interview')
# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============ MAIN ROUTES ============

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form
        return jsonify({'message': 'Message sent successfully'})
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============ API ENDPOINTS ============

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'AI Resume Builder API is running'})

@app.route('/api/user-info')
@login_required
def get_user_info():
    user_id = session.get('user_id')
    user = DatabaseHelper.fetch_one(
        "SELECT id, username, email FROM users WHERE id = %s",
        (user_id,)
    )
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# ============ STATIC FILE HANDLER ============

@app.route('/uploads/resumes/<filename>')
@login_required
def download_resume(filename):
    user_id = session.get('user_id')
    # Security check - ensure file belongs to user
    return redirect(url_for('static', filename=f'uploads/resumes/{filename}'))

# ============ TEMPLATE CONTEXT ============

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    username = session.get('username')
    return dict(user_id=user_id, username=username)

# ============ RUN APP ============

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(
        debug=debug_mode,
        host='127.0.0.1',
        port=5000,
        use_reloader=debug_mode
    )

if __name__ == '__main__':
    # For production (Render)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
