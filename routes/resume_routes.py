from flask import Blueprint, render_template, request, session, jsonify, send_file, redirect, url_for, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from utils.pdf_handler import extract_text_from_pdf
from utils.ai_analyzer import analyze_resume_with_ai
from database.db_helper import create_resume, get_resume, update_resume_analysis, delete_resume
from flask import send_file
from utils.pdf_export import generate_resume_analysis_pdf

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'static/uploads/resumes'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ UPLOAD RESUME ============

@resume_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload and process resume"""
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        try:
            if 'resume_file' not in request.files:
                flash('No file selected', 'error')
                return redirect(url_for('resume.upload'))
            
            file = request.files['resume_file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('resume.upload'))
            
            # Read file content
            resume_text = file.read().decode('utf-8', errors='ignore')
            
            # Save to database
            from database.db_helper import save_resume
            resume_id = save_resume(user_id, file.filename, resume_text)
            
            if resume_id:
                flash(f'✅ Resume uploaded! Resume ID: {resume_id}', 'success')
                return redirect(url_for('resume.analyze', resume_id=resume_id))
            else:
                flash('Failed to save resume', 'error')
                return redirect(url_for('resume.upload'))
        
        except Exception as e:
            flash(f'Error uploading resume: {str(e)[:100]}', 'error')
            return redirect(url_for('resume.upload'))
    
    return render_template('resume/upload.html')
# ============ ANALYZE RESUME ============

@resume_bp.route('/<int:resume_id>/analyze', methods=['GET', 'POST'])
@login_required
def analyze(resume_id):
    """Analyze resume using AI"""
    user_id = session['user_id']
    resume = get_resume(resume_id, user_id)
    
    if not resume:
        flash('Resume not found', 'error')
        return redirect(url_for('resume.upload'))
    
    # CHECK IF ANALYSIS ALREADY EXISTS
    if resume['ats_score'] is not None:
        # Analysis already done - DON'T RE-ANALYZE
        print(f"✅ Analysis already exists for resume {resume_id}")
        return render_template('resume/analyze.html', resume=resume)
    
    # IF NO ANALYSIS YET - RUN IT NOW
    try:
        print(f"🔍 First-time analysis for resume {resume_id}...")
        
        # Call AI analyzer
        from utils.ai_analyzer import analyze_resume_with_ai
        analysis_result = analyze_resume_with_ai(resume['original_content'])
        
        print(f"✅ Analysis Result: Score={analysis_result.get('ats_score')}")
        
        # UPDATE DATABASE - ONLY ONCE
        from database.db_helper import DatabaseHelper
        
        update_query = """
        UPDATE resumes 
        SET ats_score = %s, 
            professional_summary = %s, 
            ai_suggestions = %s, 
            job_recommendations = %s 
        WHERE id = %s AND user_id = %s
        """
        
        DatabaseHelper.execute_query(
            update_query,
            (
                analysis_result.get('ats_score', 0),
                analysis_result.get('summary', ''),
                analysis_result.get('suggestions', ''),
                analysis_result.get('jobs', ''),
                resume_id,
                user_id
            )
        )
        
        print(f"💾 Saved to database")
        
        # Get updated resume data
        resume = get_resume(resume_id, user_id)
        
        flash(f'✅ Analysis Complete! ATS Score: {resume["ats_score"]}/100', 'success')
        return render_template('resume/analyze.html', resume=resume)
    
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        flash(f'Error analyzing resume: {str(e)[:100]}', 'error')
        return redirect(url_for('resume.upload'))# ============ RESUME DETAIL ============

@resume_bp.route('/detail/<int:resume_id>')
@login_required
def detail(resume_id):
    user_id = session['user_id']
    resume = get_resume(resume_id, user_id)
    
    if not resume:
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('resume/resume_detail.html', resume=resume)

# ============ API ENDPOINTS ============

@resume_bp.route('/api/delete/<int:resume_id>', methods=['DELETE'])
@login_required
def delete_resume_api(resume_id):
    user_id = session['user_id']
    resume = get_resume(resume_id, user_id)
    
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    # Delete file
    if resume['file_path']:
        try:
            os.remove(resume['file_path'])
        except:
            pass
    
    # Delete from database
    delete_resume(resume_id, user_id)
    return jsonify({'success': True})

@resume_bp.route('/api/resumes')
@login_required
def get_resumes():
    from database.db_helper import get_user_resumes
    user_id = session['user_id']
    resumes = get_user_resumes(user_id)
    
    return jsonify({
        'resumes': resumes if resumes else []
    })
@resume_bp.route('/analyze/<int:resume_id>/export-pdf')
@login_required
def export_analysis_pdf(resume_id):
    user_id = session['user_id']
    resume = get_resume(resume_id, user_id)
    
    if not resume:
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        pdf_buffer = generate_resume_analysis_pdf(
            resume['resume_name'],
            resume['ats_score'] or 0,
            resume['professional_summary'] or 'Not analyzed',
            resume['ai_suggestions'] or 'Not analyzed',
            resume['job_recommendations'] or 'Not analyzed'
        )
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"resume_analysis_{resume_id}.pdf"
        )
    except Exception as e:
        return redirect(url_for('resume.analyze', resume_id=resume_id))
@resume_bp.route('/<int:resume_id>/delete', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """Delete a resume"""
    user_id = session['user_id']
    
    try:
        from database.db_helper import delete_resume as delete_resume_db
        result = delete_resume_db(resume_id, user_id)
        
        if result:
            flash('Resume deleted successfully!', 'success')
        else:
            flash('Resume not found', 'error')
    except Exception as e:
        flash(f'Error deleting resume: {str(e)}', 'error')
    
    return redirect(url_for('dashboard.my_resumes'))