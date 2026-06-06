from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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
                    return redirect(url_for('cover_letter.generate'))
                
                resume_text = resume['original_content'] if isinstance(resume, dict) else resume[3]
            
            # Option 2: Upload New File
            elif 'new_resume' in request.files:
                file = request.files['new_resume']
                if file.filename == '':
                    flash('❌ No file selected', 'error')
                    return redirect(url_for('cover_letter.generate'))
                
                try:
                    resume_text = file.read().decode('utf-8', errors='ignore')
                except Exception as e:
                    flash(f'❌ Error reading file: {str(e)[:100]}', 'error')
                    return redirect(url_for('cover_letter.generate'))
            
            else:
                flash('❌ Please select or upload a resume', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            if not resume_text:
                flash('❌ Resume is empty', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            if not job_title:
                flash('❌ Please enter a job title', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            # Generate cover letter
            print(f"📝 Generating cover letter for: {job_title} at {company_name}")
            cover_letter_text = generate_cover_letter(resume_text, job_title, company_name)
            
            if not cover_letter_text:
                flash('❌ Failed to generate cover letter', 'error')
                return redirect(url_for('cover_letter.generate'))
            
            # Save to database if resume_id exists
            if resume_id:
                try:
                    save_cover_letter(user_id, resume_id, job_title, company_name, cover_letter_text)
                except Exception as e:
                    print(f"Warning: Could not save to DB: {e}")
            
            flash('✅ Cover letter generated successfully!', 'success')
            return render_template('cover_letter/result.html', 
                                 cover_letter=cover_letter_text,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            print(f"❌ Cover letter error: {e}")
            import traceback
            traceback.print_exc()
            flash(f'❌ Error: {str(e)[:100]}', 'error')
            return redirect(url_for('cover_letter.generate'))
    
    return render_template('cover_letter/generate.html', resumes=resumes)
