from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from database.db_helper import get_resume, get_user_resumes
import google.generativeai as genai
import os
from dotenv import load_dotenv

cover_letter_bp = Blueprint('cover_letter', __name__)
load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@cover_letter_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        user_id = session['user_id']
        
        # Check if user is uploading new resume or selecting existing
        resume_id = request.form.get('resume_id')
        resume_text = None
        
        # Option 1: Upload new resume
        if 'resume_file' in request.files and request.files['resume_file'].filename:
            file = request.files['resume_file']
            
            if file and file.filename.endswith('.pdf'):
                try:
                    from utils.pdf_handler import extract_text_from_pdf
                    resume_text = extract_text_from_pdf(file)
                    if not resume_text:
                        return render_template('cover_letter/generate.html', 
                                             error='Could not extract text from PDF',
                                             resumes=get_user_resumes(user_id))
                except Exception as e:
                    return render_template('cover_letter/generate.html',
                                         error=f'Error reading PDF: {str(e)}',
                                         resumes=get_user_resumes(user_id))
            else:
                return render_template('cover_letter/generate.html',
                                     error='Please upload a PDF file',
                                     resumes=get_user_resumes(user_id))
        
        # Option 2: Select existing resume
        elif resume_id:
            resume = get_resume(resume_id, user_id)
            if not resume:
                return render_template('cover_letter/generate.html',
                                     error='Resume not found',
                                     resumes=get_user_resumes(user_id))
            resume_text = resume['original_content']
        
        else:
            return render_template('cover_letter/generate.html',
                                 error='Please upload or select a resume',
                                 resumes=get_user_resumes(user_id))
        
        # Get form data
        job_title = request.form.get('job_title', '').strip()
        company_name = request.form.get('company_name', '').strip()
        job_description = request.form.get('job_description', '').strip()
        
        if not job_title or not company_name:
            return render_template('cover_letter/generate.html',
                                 error='Job title and company name are required',
                                 resumes=get_user_resumes(user_id))
        
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
You are an expert career coach and professional resume writer. Write a compelling, personalized cover letter following business standards.

CANDIDATE BACKGROUND:
{resume_text[:2500]}

JOB DETAILS:
Position: {job_title}
Company: {company_name}
Description: {job_description}

REQUIREMENTS:
1. Professional business letter format with proper spacing
2. Personalized greeting (use "Dear Hiring Manager")
3. Opening paragraph: Strong hook showing enthusiasm for the specific role/company
4. Middle paragraph(s): 
   - Highlight 2-3 most relevant achievements/skills
   - Show how your experience matches job requirements
   - Include specific metrics/accomplishments
   - Demonstrate knowledge of company/industry
5. Closing paragraph: Call to action, express interest in interview
6. Professional signature block with placeholders

TONE: Professional, confident, personalized, specific (NOT generic)
LENGTH: 3-4 paragraphs, 250-400 words
FORMAT: Standard business letter format

Write only the cover letter content. Make it outstanding!
"""
            
            response = model.generate_content(prompt)
            cover_letter = response.text if response.text else "Unable to generate"
            
            return render_template('cover_letter/result.html',
                                 cover_letter=cover_letter,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            # If API quota exceeded, use mock data
            if "429" in str(e) or "quota" in str(e).lower():
                cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my solid background in relevant skills and proven track record of delivering results, I am confident I would be a valuable addition to your team.

In my professional experience, I have successfully contributed to projects that align with your company's goals. My skills in {job_title} combined with my commitment to excellence make me an ideal candidate for this role.

I am genuinely excited about the opportunity to contribute to {company_name}'s continued success. I would welcome the chance to discuss how my experience and skills can benefit your organization.

Thank you for considering my application. I look forward to hearing from you soon.

Sincerely,
[Your Name]"""
                
                flash('⚠️ Using template - API quota exceeded (resets in 24 hours)', 'warning')
                
                return render_template('cover_letter/result.html',
                                     cover_letter=cover_letter,
                                     job_title=job_title,
                                     company_name=company_name)
            else:
                return render_template('cover_letter/generate.html',
                                     error=f'Error: {str(e)[:100]}',
                                     resumes=get_user_resumes(user_id))
    
    user_id = session['user_id']
    resumes = get_user_resumes(user_id)
    return render_template('cover_letter/generate.html', resumes=resumes)