# 🤖 AI Resume Builder

An advanced AI-powered resume analyzer that helps job seekers optimize their resumes using Google Gemini AI. Get instant ATS scores, professional summaries, improvement suggestions, and personalized job recommendations.

## ✨ Features

- **📤 Resume Upload**: Upload PDF resumes for instant analysis
- **🤖 AI Analysis**: Advanced analysis powered by Google Gemini AI
- **📊 ATS Score**: Get Applicant Tracking System compatibility score (0-100)
- **💡 Smart Suggestions**: Receive AI-generated improvement recommendations
- **⭐ Professional Summary**: Auto-generated professional summaries
- **💼 Job Recommendations**: Get personalized job title suggestions
- **👤 User Accounts**: Secure registration and login system
- **📁 Resume History**: Manage multiple resumes
- **📱 Responsive Design**: Works on all devices

## 🛠️ Tech Stack

- **Backend**: Python Flask 2.3+
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: Google Gemini API
- **PDF Processing**: PyPDF2
- **Authentication**: Werkzeug

## 📋 Prerequisites

- Python 3.8+
- MySQL Server 8.0+
- MySQL Workbench (optional, for database management)
- Google Gemini API Key

## 🚀 Quick Start

### 1. Clone or Download Project

```bash
cd ai-resume-builder
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

**Using MySQL Workbench:**
1. Open MySQL Workbench
2. Create a new connection to localhost:3306
3. Execute the script in `database/schema.sql`

**Using Command Line:**
```bash
mysql -u root -p < database/schema.sql
```

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Edit `.env` and fill in your credentials:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=ai_resume_builder
MYSQL_PORT=3306
GEMINI_API_KEY=your_gemini_key_here
```

**Get Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste in `.env`

### 6. Run the Application

```bash
python app.py
```

Visit: `http://localhost:5000`

## 📁 Project Structure

```
ai-resume-builder/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
│
├── config/                  # Configuration files
│   └── settings.py         # Flask settings
│
├── routes/                  # API routes
│   ├── auth_routes.py      # Authentication
│   ├── resume_routes.py    # Resume operations
│   └── dashboard_routes.py # Dashboard
│
├── templates/               # HTML templates
│   ├── auth/               # Auth pages
│   ├── resume/             # Resume pages
│   └── components/         # Reusable components
│
├── static/                  # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript
│   └── uploads/resumes/    # Uploaded PDFs
│
├── utils/                   # Utility modules
│   ├── ai_analyzer.py      # Gemini AI integration
│   ├── pdf_handler.py      # PDF processing
│   └── validators.py       # Input validation
│
├── database/                # Database files
│   ├── db_config.py        # DB configuration
│   ├── db_helper.py        # DB operations
│   └── schema.sql          # Database schema
│
└── docs/                    # Documentation
```

## 🔑 Key Features Explained

### ATS Score
The ATS (Applicant Tracking System) score (0-100) indicates how well your resume is optimized to pass through automated resume scanning systems used by recruiters.

### AI Suggestions
Personalized improvement recommendations based on your resume content, formatting, and industry best practices.

### Professional Summary
Auto-generated professional summary that highlights your key qualifications.

### Job Recommendations
Get job titles that match your skills and experience profile.

## 🔐 Security

- Passwords hashed with Werkzeug
- SQL injection protection with parameterized queries
- CSRF protection enabled
- Secure session management
- File upload validation

## 📱 Responsive Design

Works seamlessly on:
- Desktop computers
- Tablets
- Mobile devices

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### "Connection refused" MySQL error
- Check if MySQL server is running
- Verify connection settings in `.env`
- Use `mysql -u root -p` to test

### "Module not found" errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Gemini API key errors
- Verify API key in `.env`
- Check if API is enabled in Google Cloud
- Ensure key has Generative AI permissions

### Resume upload fails
- Check file is valid PDF
- Ensure file size < 16MB
- Try extracting text manually to verify PDF quality

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in console
3. Check MySQL Workbench for database issues

## 🎯 Future Enhancements

- [ ] Cover letter generator
- [ ] LinkedIn profile optimization
- [ ] Interview preparation
- [ ] Resume templates
- [ ] Export to Word/PDF
- [ ] Batch resume analysis
- [ ] Email notifications
- [ ] Payment integration for premium features

## 📊 Database Schema

### Users Table
- id, username, email, password, bio, created_at

### Resumes Table
- id, user_id, resume_name, original_content, ai_suggestions, ats_score, professional_summary, job_recommendations, created_at

### Skills Table
- id, resume_id, skill_name, proficiency, category

### Analytics Table
- id, user_id, action, details, created_at

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Google Gemini API: https://ai.google.dev/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/

## 💡 Tips for Best Results

1. Use a professional resume format
2. Include specific metrics and achievements
3. Use industry-relevant keywords
4. Keep resume to 1-2 pages
5. Use standard fonts (Arial, Times New Roman, Calibri)
6. Ensure PDF is text-based (not scanned image)

---

**Built with ❤️ using Flask & Google Gemini AI**

Happy Resume Building! 🚀
