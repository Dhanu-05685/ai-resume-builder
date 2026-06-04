from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime

def generate_cover_letter_pdf(cover_letter_text, job_title, company_name):
    """Generate PDF from cover letter text"""
    
    # Create PDF in memory
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#667eea',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_LEFT
    )
    
    # Title
    title = Paragraph(f"Cover Letter - {company_name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Date and info
    date_text = Paragraph(f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", body_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.2*inch))
    
    # Job title
    job_text = Paragraph(f"<b>Position:</b> {job_title}", body_style)
    elements.append(job_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Cover letter content
    content = Paragraph(cover_letter_text.replace('\n', '<br/>'), body_style)
    elements.append(content)
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return pdf_buffer

def generate_resume_analysis_pdf(resume_name, ats_score, summary, suggestions, jobs):
    """Generate PDF from resume analysis"""
    
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#667eea',
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='#764ba2',
        spaceAfter=10,
        spaceBefore=15
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    
    # Title
    title = Paragraph(f"Resume Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Resume name
    name = Paragraph(f"<b>Resume:</b> {resume_name}", body_style)
    elements.append(name)
    
    # ATS Score
    ats_text = Paragraph(f"<b>ATS Score:</b> {ats_score}/100", body_style)
    elements.append(ats_text)
    elements.append(Spacer(1, 0.2*inch))
    
    # Professional Summary
    summary_heading = Paragraph("Professional Summary", heading_style)
    elements.append(summary_heading)
    summary_para = Paragraph(summary, body_style)
    elements.append(summary_para)
    elements.append(Spacer(1, 0.2*inch))
    
    # Suggestions
    suggestions_heading = Paragraph("Improvement Suggestions", heading_style)
    elements.append(suggestions_heading)
    suggestions_para = Paragraph(suggestions.replace('\n', '<br/>'), body_style)
    elements.append(suggestions_para)
    elements.append(Spacer(1, 0.2*inch))
    
    # Recommended Jobs
    jobs_heading = Paragraph("Recommended Job Titles", heading_style)
    elements.append(jobs_heading)
    jobs_para = Paragraph(jobs, body_style)
    elements.append(jobs_para)

    pdf_buffer = generate_resume_analysis_pdf(
    resume['resume_name'],
    resume['ats_score'] if resume['ats_score'] is not None else 0,
    resume['professional_summary'] if resume['professional_summary'] else 'Not analyzed',
    resume['ai_suggestions'] if resume['ai_suggestions'] else 'Not analyzed',
    resume['job_recommendations'] if resume['job_recommendations'] else 'Not analyzed'
)
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return pdf_buffer