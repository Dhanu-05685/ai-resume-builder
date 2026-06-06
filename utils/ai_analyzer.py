import google.generativeai as genai
import os
import json
import re
import hashlib
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')
if API_KEY:
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel('gemini-2.5-flash')
else:
    MODEL = None

def parse_resume_content(resume_text):
    """Parse resume and extract actual data from it"""
    text = resume_text
    text_lower = resume_text.lower()
    
    parsed = {
        'full_text': text,
        'work_experience': extract_section(text, ['experience', 'work history', 'professional experience']),
        'education': extract_section(text, ['education', 'academic', 'degree']),
        'skills': extract_section(text, ['skills', 'technical skills', 'core competencies']),
        'projects': extract_section(text, ['projects', 'portfolio']),
        'certifications': extract_section(text, ['certification', 'certified', 'credentials']),
        'summary': extract_section(text, ['summary', 'objective', 'professional summary'])
    }
    
    return parsed

def extract_section(text, keywords):
    """Extract specific section from resume"""
    text_lower = text.lower()
    
    for keyword in keywords:
        idx = text_lower.find(keyword)
        if idx != -1:
            start = idx + len(keyword)
            end_idx = start
            for i in range(start, min(start + 1000, len(text))):
                if i > start + 500 and text[i] == '\n':
                    end_idx = i
                    break
            if end_idx == start:
                end_idx = min(start + 1000, len(text))
            
            return text[start:end_idx].strip()
    
    return ""

def analyze_resume_with_ai(resume_text):
    """Analyze resume and return unique analysis per resume"""
    
    try:
        if MODEL and API_KEY:
            return analyze_with_gemini(resume_text)
    except Exception as e:
        print(f"⚠️ API unavailable: {str(e)[:50]}")
    
    return analyze_locally(resume_text)

def analyze_with_gemini(resume_text):
    """Use Gemini API to analyze resume"""
    
    prompt = f"""Analyze this resume CAREFULLY and provide JSON:

RESUME:
{resume_text[:3000]}

Respond with ONLY valid JSON:
{{
    "ats_score": <0-100>,
    "job_titles": "<job titles>",
    "professional_summary": "<summary>",
    "improvements": "<improvements>"
}}"""
    
    response = MODEL.generate_content(prompt)
    text = response.text.strip()
    
    if '```' in text:
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    
    try:
        data = json.loads(text.strip())
        return {
            'ats_score': min(100, max(30, int(data.get('ats_score', 72)))),
            'jobs': data.get('job_titles', 'Software Engineer'),
            'summary': data.get('professional_summary', ''),
            'suggestions': data.get('improvements', '')
        }
    except:
        return analyze_locally(resume_text)

def analyze_locally(resume_text):
    """Smart local analysis that reads actual resume content"""
    
    parsed = parse_resume_content(resume_text)
    
    ats_score = calculate_smart_ats_score(resume_text, parsed)
    job_titles = extract_actual_job_titles(parsed['work_experience'])
    recommended_jobs = recommend_jobs_based_on_experience(parsed, job_titles)
    summary = generate_smart_summary(parsed)
    suggestions = generate_specific_suggestions(parsed, ats_score)
    
    return {
        'ats_score': ats_score,
        'jobs': recommended_jobs,
        'summary': summary,
        'suggestions': suggestions
    }

def calculate_smart_ats_score(resume_text, parsed):
    """Calculate ATS score - CONSISTENT algorithm"""
    
    # CREATE HASH FOR CONSISTENCY - Same resume always gets same score
    resume_hash = hashlib.md5(resume_text.encode()).hexdigest()
    print(f"📝 Resume Hash: {resume_hash[:8]}... (ensures consistency)")
    
    score = 40
    text_lower = resume_text.lower()
    
    # 1. WORK EXPERIENCE (25 points max)
    exp_length = len(parsed['work_experience'].split())
    print(f"   Experience words: {exp_length}")
    
    if exp_length > 150:
        score += 20
    elif exp_length > 100:
        score += 15
    elif exp_length > 50:
        score += 10
    else:
        score += 5
    
    # 2. EDUCATION (15 points max)
    if parsed['education']:
        score += 10
        print(f"   ✓ Education section found")
        
        if 'phd' in text_lower:
            score += 5
            print(f"   ✓ PhD detected")
        elif 'master' in text_lower:
            score += 3
            print(f"   ✓ Master's degree detected")
        elif 'bachelor' in text_lower or 'bs' in text_lower or 'ba' in text_lower:
            score += 2
            print(f"   ✓ Bachelor's degree detected")
    
    # 3. CERTIFICATIONS (10 points max)
    if parsed['certifications']:
        score += 8
        print(f"   ✓ Certifications found")
    
    # 4. METRICS & ACHIEVEMENTS (15 points max)
    metrics = len(re.findall(r'\d+%|\$\d+|increased|improved|reduced|grew|scaled', 
                             parsed['work_experience'].lower()))
    metric_points = min(metrics * 2, 15)
    score += metric_points
    print(f"   Metrics found: {metrics} ({metric_points} points)")
    
    # 5. ACTION VERBS (15 points max)
    verbs = ['led', 'managed', 'developed', 'designed', 'implemented', 'created', 
             'built', 'improved', 'increased', 'achieved', 'directed', 'coordinated']
    verb_count = sum(1 for verb in verbs if f' {verb} ' in f' {parsed["work_experience"].lower()} ')
    verb_points = min(verb_count * 2, 15)
    score += verb_points
    print(f"   Action verbs found: {verb_count} ({verb_points} points)")
    
    # 6. SKILLS (15 points max)
    if parsed['skills']:
        score += 10
        print(f"   ✓ Skills section found")
        
        skills_count = len([s for s in parsed['skills'].split(',') if s.strip()])
        skill_points = min(skills_count, 5)
        score += skill_points
        print(f"   Skills count: {skills_count} ({skill_points} points)")
    
    # 7. PROJECTS (5 points max)
    if parsed['projects']:
        score += 5
        print(f"   ✓ Projects section found")
    
    # 8. LENGTH & CONTENT (10 points max)
    word_count = len(resume_text.split())
    print(f"   Total words: {word_count}")
    
    if 500 <= word_count <= 2000:
        score += 10
        print(f"   ✓ Ideal word count (500-2000)")
    elif word_count < 300:
        score -= 10
        print(f"   ✗ Too short (< 300 words)")
    elif word_count > 2500:
        score += 5
        print(f"   Acceptable word count")
    
    # FINAL SCORE
    final_score = min(100, max(30, score))
    print(f"✅ Final ATS Score: {final_score}/100\n")
    
    return final_score

def extract_actual_job_titles(work_experience_text):
    """Extract job titles from work experience"""
    text = work_experience_text
    
    patterns = [
        r'(?:position|role|title):\s*([^\n]+)',
        r'^(?:•|-|\*)\s*([^•\n]*(?:engineer|developer|manager|lead|architect|analyst|specialist|director|coordinator)[^\n]*)',
        r'(?:as|as a)\s+([a-z\s]+?)(?:\s+at|\s+with|\s+in|$)',
    ]
    
    found_titles = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        found_titles.extend(matches)
    
    found_titles = [title.strip() for title in found_titles if title.strip() and len(title) > 3]
    found_titles = [t for t in found_titles if not t.lower().startswith('at ')]
    
    return list(set(found_titles))[:5]

def recommend_jobs_based_on_experience(parsed, job_titles):
    """Recommend jobs based on actual experience"""
    
    recommendations = set()
    
    # Add variations of current job titles
    for title in job_titles:
        title_lower = title.lower()
        recommendations.add(title)
        print(f"   Found job title: {title}")
        
        # Suggest progressions
        if 'junior' in title_lower:
            recommendations.add(title.replace('junior', 'senior').replace('Junior', 'Senior'))
        if 'developer' in title_lower:
            recommendations.add('Senior Developer')
            recommendations.add('Technical Lead')
        if 'engineer' in title_lower:
            recommendations.add('Senior Engineer')
            recommendations.add('Engineering Manager')
    
    # Analyze skills for additional recommendations
    skills_text = (parsed['skills'] + ' ' + parsed['work_experience']).lower()
    
    if 'python' in skills_text or 'java' in skills_text or 'c++' in skills_text:
        recommendations.add('Software Engineer')
        recommendations.add('Backend Developer')
    
    if 'javascript' in skills_text or 'react' in skills_text or 'vue' in skills_text:
        recommendations.add('Frontend Developer')
        recommendations.add('Full Stack Developer')
    
    if 'aws' in skills_text or 'azure' in skills_text or 'gcp' in skills_text or 'docker' in skills_text:
        recommendations.add('DevOps Engineer')
        recommendations.add('Cloud Architect')
        recommendations.add('Infrastructure Engineer')
    
    if 'data' in skills_text or 'sql' in skills_text or 'database' in skills_text:
        recommendations.add('Data Engineer')
        recommendations.add('Database Administrator')
        recommendations.add('Analytics Engineer')
    
    if 'led' in skills_text or 'managed' in skills_text or 'team' in skills_text:
        recommendations.add('Technical Lead')
        recommendations.add('Engineering Manager')
        recommendations.add('Project Manager')
    
    if 'product' in skills_text or 'strategy' in skills_text:
        recommendations.add('Product Manager')
    
    # Remove duplicates and limit to 6
    recommendations = set(r for r in recommendations if r.strip())
    
    if not recommendations:
        recommendations = {'Software Engineer', 'Developer', 'Technical Professional'}
    
    return ', '.join(list(recommendations)[:6])

def generate_smart_summary(parsed):
    """Generate summary based on actual resume"""
    
    exp_text = parsed['work_experience'].lower()
    skills_text = parsed['skills']
    
    if exp_text and skills_text:
        # Extract first skill
        first_skill = skills_text.split(',')[0].strip() if skills_text else 'technology'
        
        # Extract key responsibility
        if 'led' in exp_text or 'managed' in exp_text:
            return f"Results-driven professional with expertise in {first_skill}. Proven track record of leading teams and delivering impactful solutions. Strong strategic thinker with focus on driving organizational goals."
        elif 'developed' in exp_text or 'designed' in exp_text:
            return f"Experienced professional with deep expertise in {first_skill}. Demonstrated success in designing and implementing scalable solutions. Committed to technical excellence and continuous innovation."
        else:
            return f"Experienced professional with expertise in {first_skill}. Proven track record of delivering quality solutions and driving measurable impact. Skilled in implementing and managing complex projects."
    
    elif exp_text:
        return "Dedicated professional with strong work experience and proven ability to deliver results. Committed to excellence and continuous improvement."
    else:
        return "Professional with technical background and commitment to quality. Seeking opportunities to grow and make meaningful contributions."

def generate_specific_suggestions(parsed, ats_score):
    """Generate specific suggestions based on resume content"""
    suggestions = []
    
    exp_length = len(parsed['work_experience'].split())
    ed_length = len(parsed['education'].split())
    skills_length = len([s for s in parsed['skills'].split(',') if s.strip()])
    cert_length = len(parsed['certifications'].split())
    
    print("📊 Resume Analysis:")
    print(f"   Experience length: {exp_length} words")
    print(f"   Education length: {ed_length} words")
    print(f"   Skills count: {skills_length}")
    print(f"   Certifications: {cert_length}")
    
    if exp_length < 50:
        suggestions.append('• Expand work experience section with detailed achievements and quantifiable results')
    
    if ed_length < 20:
        suggestions.append('• Add education details: degree type, institution name, and graduation year')
    
    if skills_length < 5:
        suggestions.append('• Include more technical and professional skills (aim for 8-12 skills)')
    
    if cert_length == 0:
        suggestions.append('• Add relevant certifications or licenses to strengthen your profile')
    
    if not re.search(r'\d+%|\$\d+|increased|improved|reduced', parsed['work_experience']):
        suggestions.append('• Quantify achievements with specific metrics, percentages, and measurable impact')
    
    if not re.search(r'led|managed|directed|supervised', parsed['work_experience']):
        suggestions.append('• Highlight leadership experience and team management responsibilities')
    
    if not parsed['projects']:
        suggestions.append('• Add a projects section showcasing key accomplishments and technical work')
    
    if ats_score < 50:
        suggestions.append('• Review resume structure and formatting for clarity and ATS compatibility')
    
    if not suggestions:
        if ats_score >= 80:
            suggestions.append('• Resume is well-optimized - maintain current quality and structure')
        else:
            suggestions.append('• Continue adding quantifiable achievements and expanding experience details')
    
    return '\n'.join(suggestions[:5])

def extract_key_skills(resume_text):
    """Extract skills from resume"""
    parsed = parse_resume_content(resume_text)
    skills = parsed['skills'].split(',')
    return [s.strip() for s in skills if s.strip()][:10]

def generate_cover_letter(resume_text, job_title, company_name=""):
    """Generate cover letter"""
    try:
        if MODEL and API_KEY:
            prompt = f"Generate cover letter for {job_title} at {company_name}. Resume: {resume_text[:1000]}"
            response = MODEL.generate_content(prompt)
            return response.text
    except:
        pass
    
    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. 
With my professional experience and proven skills, I am confident I can make significant contributions.

My background has equipped me with the expertise required to excel in this role. 
I am excited about the opportunity to contribute to your organization's success.

Thank you for your consideration.

Sincerely,
[Your Name]"""

def generate_interview_prep(resume_text, job_title, company_name=''):
    """Generate interview questions, tips, and sample answers"""
    try:
        prompt = f"""
Based on this resume and job position, generate comprehensive interview preparation:

RESUME:
{resume_text[:2000]}

JOB TITLE: {job_title}
COMPANY: {company_name if company_name else 'Not specified'}

Please provide in JSON format ONLY (no markdown, no extra text):
{{
    "questions": "List 5-7 interview questions likely to be asked. Format: 1. Question? 2. Question? etc.",
    "tips": "5-7 tips for answering interview questions. Format: 1. Tip 2. Tip etc.",
    "answers": "Sample answers framework for common questions asked for {job_title} role."
}}

IMPORTANT: Return ONLY valid JSON, nothing else.
"""
        
        # Try Gemini API
        try:
            response = genai.generate_text(prompt=prompt, max_output_tokens=1000)
            
            if response and response.result:
                import json
                text = response.result.strip()
                
                # Extract JSON if wrapped in markdown
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0]
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0]
                
                data = json.loads(text)
                return {
                    'questions': data.get('questions', 'No questions generated'),
                    'tips': data.get('tips', 'No tips generated'),
                    'answers': data.get('answers', 'No sample answers generated')
                }
        except Exception as e:
            print(f"⚠️ Gemini API failed: {e}, using local generation")
        
        # LOCAL FALLBACK
        questions = f"""
1. Tell me about your experience with {job_title.lower()} work
2. What are your strengths for a {job_title} role?
3. Describe your most challenging project related to {job_title}
4. How do you stay updated with latest technologies?
5. Why do you want to work at {company_name if company_name else 'our company'}?
6. What are your salary expectations?
7. Where do you see yourself in 5 years?
"""
        
        tips = """
1. Use STAR method (Situation, Task, Action, Result) for behavioral questions
2. Research the company and role thoroughly before the interview
3. Practice your answers but don't memorize them completely
4. Ask thoughtful questions about the role and company
5. Maintain eye contact and positive body language
6. Show enthusiasm and genuine interest in the position
7. Follow up with a thank-you email after the interview
"""
        
        answers = f"""
Sample Framework for {job_title}:
- Highlight relevant experience and skills from your resume
- Use specific examples and metrics to demonstrate impact
- Show problem-solving abilities and how you handle challenges
- Emphasize learning and growth mindset
- Connect your skills directly to the job requirements
"""
        
        return {
            'questions': questions,
            'tips': tips,
            'answers': answers
        }
    
    except Exception as e:
        print(f"❌ Interview prep error: {e}")
        return None