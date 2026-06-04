from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps
from database.db_helper import get_resume, get_user_resumes
import google.generativeai as genai
import os
from dotenv import load_dotenv

interview_bp = Blueprint('interview', __name__)
load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@interview_bp.route('/prep', methods=['GET', 'POST'])
@login_required
def prep():
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
                        return render_template('interview/prep.html',
                                             error='Could not extract text from PDF',
                                             resumes=get_user_resumes(user_id))
                except Exception as e:
                    return render_template('interview/prep.html',
                                         error=f'Error reading PDF: {str(e)}',
                                         resumes=get_user_resumes(user_id))
            else:
                return render_template('interview/prep.html',
                                     error='Please upload a PDF file',
                                     resumes=get_user_resumes(user_id))
        
        # Option 2: Select existing resume
        elif resume_id:
            resume = get_resume(resume_id, user_id)
            if not resume:
                return render_template('interview/prep.html',
                                     error='Resume not found',
                                     resumes=get_user_resumes(user_id))
            resume_text = resume['original_content']
        
        else:
            return render_template('interview/prep.html',
                                 error='Please upload or select a resume',
                                 resumes=get_user_resumes(user_id))
        
        # Get form data
        job_title = request.form.get('job_title', '').strip()
        company_name = request.form.get('company_name', '').strip()
        
        if not job_title or not company_name:
            return render_template('interview/prep.html',
                                 error='Job title and company name are required',
                                 resumes=get_user_resumes(user_id))
        
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Generate interview questions
            q_prompt = f"""
Generate 7 tough, realistic interview questions for a {job_title} position based on this candidate:

{resume_text[:2000]}

Format each question on a new line starting with "Q:"
Make questions specific to their background and the role.
"""
            
            q_response = model.generate_content(q_prompt)
            questions = q_response.text if q_response.text else ""
            
            # Generate interview tips
            t_prompt = f"""
Give 8 specific, actionable interview tips for a {job_title} position at {company_name}.

Consider this background:
{resume_text[:1500]}

Format as numbered list (1-8). Make tips specific and practical.
"""
            
            t_response = model.generate_content(t_prompt)
            tips = t_response.text if t_response.text else ""
            
            # Generate sample answers
            a_prompt = f"""
Generate excellent sample answers to common interview questions for a {job_title} at {company_name}.

Candidate background:
{resume_text[:2000]}

Questions to answer:
1. Tell me about yourself
2. Why do you want this job?
3. What are your greatest strengths?
4. Tell me about a challenge you overcame
5. How do you handle pressure/tight deadlines?
6. What are your weaknesses and how do you improve?
7. Where do you see yourself in 5 years?

Provide professional, concise, STAR-method answers that showcase their unique background.
"""
            
            a_response = model.generate_content(a_prompt)
            answers = a_response.text if a_response.text else ""
            
            return render_template('interview/result.html',
                                 questions=questions,
                                 tips=tips,
                                 answers=answers,
                                 job_title=job_title,
                                 company_name=company_name)
        
        except Exception as e:
            # If API quota exceeded, use mock data
            if "429" in str(e) or "quota" in str(e).lower():
                questions = """
Q1: Tell me about yourself and your relevant experience
Q2: Why are you interested in this {job_title} position?
Q3: What are your greatest strengths for this role?
Q4: Can you describe a challenging project you completed?
Q5: How do you stay updated with industry trends?
Q6: What are your weaknesses and how do you address them?
Q7: Where do you see yourself in 5 years?
""".format(job_title=job_title)
                
                tips = """
1. Research the company thoroughly before the interview
2. Practice answering common interview questions
3. Use the STAR method for behavioral questions
4. Prepare specific examples from your experience
5. Ask thoughtful questions about the role and company
6. Maintain good eye contact and positive body language
7. Send a thank you email after the interview
8. Be authentic and let your personality shine through
"""
                
                answers = """
Sample answers will be provided once the API quota resets (in 24 hours).
For now, prepare using the STAR method: Situation, Task, Action, Result.
"""
                
                flash('⚠️ Using template - API quota exceeded (resets in 24 hours)', 'warning')
                
                return render_template('interview/result.html',
                                     questions=questions,
                                     tips=tips,
                                     answers=answers,
                                     job_title=job_title,
                                     company_name=company_name)
            else:
                return render_template('interview/prep.html',
                                     error=f'Error: {str(e)[:100]}',
                                     resumes=get_user_resumes(user_id))
    
    user_id = session['user_id']
    resumes = get_user_resumes(user_id)
    return render_template('interview/prep.html', resumes=resumes)