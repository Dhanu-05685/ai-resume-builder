from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from database.db_helper import get_user_resumes, get_resume
from utils.ai_analyzer import generate_interview_prep

interview_bp = Blueprint('interview', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@interview_bp.route('/prep', methods=['GET', 'POST'])
@login_required
def prep():
    """Interview preparation"""
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
                return redirect(url_for('interview.prep'))
            
            # Get resume content
            resume = get_resume(int(resume_id), user_id)
            if not resume:
                flash('Resume not found', 'error')
                return redirect(url_for('interview.prep'))
            
            # Generate interview prep
            resume_text = resume['original_content'] if isinstance(resume, dict) else resume[3]
            prep_data = generate_interview_prep(resume_text, job_title, company_name)
            
            if not prep_data:
                flash('Failed to generate interview prep', 'error')
                return redirect(url_for('interview.prep'))
            
            flash('✅ Interview prep generated successfully!', 'success')
            return render_template('interview/result.html', 
                                 prep=prep_data,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            print(f"❌ Interview prep error: {e}")
            flash(f'Error: {str(e)[:100]}', 'error')
            return redirect(url_for('interview.prep'))
    
    return render_template('interview/prep.html', resumes=resumes)