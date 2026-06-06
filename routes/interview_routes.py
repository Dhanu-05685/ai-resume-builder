from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from database.db_helper import get_user_resumes, get_resume, save_interview_prep
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
    resumes = get_user_resumes(user_id) or []
    
    if request.method == 'POST':
        try:
            resume_text = None
            resume_id = None
            job_title = request.form.get('job_title', '').strip()
            company_name = request.form.get('company_name', '').strip()
            
            # Option 1: Select Existing Resume
            if request.form.get('resume_id'):
                resume_id = int(request.form.get('resume_id'))
                resume = get_resume(resume_id, user_id)
                
                if not resume:
                    flash('❌ Resume not found', 'error')
                    return redirect(url_for('interview.prep'))
                
                resume_text = resume['original_content'] if isinstance(resume, dict) else resume[3]
            
            # Option 2: Upload New File
            elif 'new_resume' in request.files:
                file = request.files['new_resume']
                if file.filename == '':
                    flash('❌ No file selected', 'error')
                    return redirect(url_for('interview.prep'))
                
                try:
                    resume_text = file.read().decode('utf-8', errors='ignore')
                except Exception as e:
                    flash(f'❌ Error reading file: {str(e)[:100]}', 'error')
                    return redirect(url_for('interview.prep'))
            
            else:
                flash('❌ Please select or upload a resume', 'error')
                return redirect(url_for('interview.prep'))
            
            if not resume_text:
                flash('❌ Resume is empty', 'error')
                return redirect(url_for('interview.prep'))
            
            if not job_title:
                flash('❌ Please enter a job title', 'error')
                return redirect(url_for('interview.prep'))
            
            # Generate interview prep
            print(f"📝 Generating interview prep for: {job_title} at {company_name}")
            prep_data = generate_interview_prep(resume_text, job_title, company_name)
            
            if not prep_data:
                flash('❌ Failed to generate interview prep', 'error')
                return redirect(url_for('interview.prep'))
            
            # Save to database if resume_id exists
            if resume_id:
                try:
                    save_interview_prep(
                        user_id, 
                        resume_id, 
                        job_title, 
                        company_name,
                        prep_data.get('questions', ''),
                        prep_data.get('tips', ''),
                        prep_data.get('answers', '')
                    )
                except Exception as e:
                    print(f"Warning: Could not save to DB: {e}")
            
            flash('✅ Interview prep generated successfully!', 'success')
            return render_template('interview/result.html', 
                                 prep=prep_data,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            print(f"❌ Interview prep error: {e}")
            import traceback
            traceback.print_exc()
            flash(f'❌ Error: {str(e)[:100]}', 'error')
            return redirect(url_for('interview.prep'))
    
    return render_template('interview/prep.html', resumes=resumes)