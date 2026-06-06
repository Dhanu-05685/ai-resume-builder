from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from database.db_helper import get_user_resumes, get_resume, save_cover_letter
from utils.ai_analyzer import generate_cover_letter

cover_letter_bp = Blueprint('cover_letter', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@cover_letter_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    """Generate cover letter"""
    user_id = session.get('user_id')
    
    # Get user's resumes
    resumes = get_user_resumes(user_id)
    if not resumes:
        resumes = []
    
    if request.method == 'POST':
        try:
            resume_id = request.form.get('resume_id')
            job_title = request.form.get('job_title', '')
            company_name = request.form.get('company_name', '')
            
            if not resume_id:
                flash('Please select a resume', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            # Get resume content
            resume = get_resume(int(resume_id), user_id)
            if not resume:
                flash('Resume not found', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            # Generate cover letter
            resume_text = resume['original_content'] if isinstance(resume, dict) else resume[3]
            cover_letter_text = generate_cover_letter(resume_text, job_title, company_name)
            
            if not cover_letter_text:
                flash('Failed to generate cover letter', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            # Save to database
            save_cover_letter(user_id, int(resume_id), job_title, company_name, cover_letter_text)
            
            flash('✅ Cover letter generated successfully!', 'success')
            return render_template('cover_letter/result.html', 
                                 cover_letter=cover_letter_text,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            print(f"❌ Cover letter error: {e}")
            flash(f'Error: {str(e)[:100]}', 'error')
            return redirect(url_for('cover_letter.generate'))
    
    return render_template('cover_letter/generate.html', resumes=resumes)