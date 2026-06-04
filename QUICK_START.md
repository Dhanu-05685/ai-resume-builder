# 📦 AI Resume Builder - Complete Package

## ✅ What's Included

Your AI Resume Builder project includes a **production-ready** Flask application with:

### 🎯 Core Features
- ✅ User authentication (Sign up, Login, Logout)
- ✅ Resume upload (PDF support)
- ✅ AI-powered analysis using Google Gemini
- ✅ ATS score calculation (0-100)
- ✅ Professional summary generation
- ✅ Job recommendations
- ✅ Resume management dashboard
- ✅ Responsive design (mobile, tablet, desktop)

### 📁 Complete File Structure
```
ai-resume-builder/
├── app.py                      # Main Flask application
├── requirements.txt            # All dependencies
├── .env.example               # Environment template
├── README.md                  # Full documentation
├── QUICK_START.md             # This file
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration file
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py         # Login/Signup routes
│   ├── resume_routes.py       # Resume operations
│   └── dashboard_routes.py    # Dashboard routes
│
├── templates/                 # 13 HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── 404.html               # Error page
│   ├── 500.html               # Server error
│   ├── auth/
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── forgot_password.html
│   ├── resume/
│   │   ├── upload.html
│   │   ├── analyze.html
│   │   ├── dashboard.html
│   │   ├── my_resumes.html
│   │   └── resume_detail.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
│
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling
│   ├── js/
│   │   └── main.js            # JavaScript utilities
│   └── uploads/resumes/       # Where PDFs are stored
│
├── utils/
│   ├── __init__.py
│   ├── ai_analyzer.py         # Google Gemini integration
│   ├── pdf_handler.py         # PDF text extraction
│   └── validators.py          # Input validation
│
├── database/
│   ├── __init__.py
│   ├── db_config.py           # Database connection
│   ├── db_helper.py           # Query functions
│   └── schema.sql             # Database creation script
│
├── models/                    # (For future use)
├── services/                  # (For future use)
└── tests/                     # (For future use)
```

---

## 🚀 QUICK START (5 MINUTES)

### Step 1: Install MySQL & Create Database

**Windows:**
1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
2. Install with default settings
3. Note your password
4. Open MySQL Command Line or Workbench

**Mac (using Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

### Step 2: Create Database

**Using MySQL Workbench:**
1. Open MySQL Workbench
2. Create new connection (localhost:3306)
3. Open `database/schema.sql`
4. Execute the script

**Using Command Line:**
```bash
mysql -u root -p < database/schema.sql
```

Enter your MySQL password when prompted.

### Step 3: Get Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key

### Step 4: Setup Python Project

```bash
# Navigate to project
cd ai-resume-builder

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Configure Environment

1. Copy `.env.example` to `.env`
2. Edit `.env` and replace values:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-123
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=ai_resume_builder
MYSQL_PORT=3306
GEMINI_API_KEY=paste_your_key_here
```

### Step 6: Run Application

```bash
python app.py
```

**Output should show:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 7: Test It Out

1. Open: http://localhost:5000
2. Click **"Sign Up"**
3. Create an account
4. Click **"Upload Resume"**
5. Upload a PDF resume
6. View AI analysis results! 🎉

---

## 🔧 Configuration Guide

### .env File Reference

| Variable | Value | Example |
|----------|-------|---------|
| `FLASK_ENV` | development or production | development |
| `SECRET_KEY` | Random string for session | abc123xyz789 |
| `MYSQL_HOST` | Database host | localhost |
| `MYSQL_USER` | Database user | root |
| `MYSQL_PASSWORD` | Database password | mypassword |
| `MYSQL_DATABASE` | Database name | ai_resume_builder |
| `MYSQL_PORT` | Database port | 3306 |
| `GEMINI_API_KEY` | Google Gemini API key | (from makersuite.google.com) |

---

## 🗄️ Database Setup

### Using MySQL Workbench (Easiest)

1. Open MySQL Workbench
2. Click: Database → Create New → Physical Schema
3. Name: `ai_resume_builder`
4. Click Create
5. File → Open SQL Script → Select `database/schema.sql`
6. Execute (Lightning bolt icon)
7. ✅ Done!

### Using Command Line

```bash
# Login to MySQL
mysql -u root -p

# Run database creation
mysql -u root -p < database/schema.sql

# Verify
mysql -u root -p
> USE ai_resume_builder;
> SHOW TABLES;
```

---

## 📦 Dependencies Included

```
Flask==2.3.3              # Web framework
MySQL-Connector==8.1.0    # MySQL connection
PyPDF2==3.0.1             # PDF reading
google-generativeai==0.3.0 # Gemini AI
python-dotenv==1.0.0      # Environment variables
Werkzeug==2.3.7           # Password hashing
```

All included in `requirements.txt`

---

## 🎯 Project Features Breakdown

### 🔐 Authentication
- Secure password hashing
- Session management
- Email validation
- Password strength checker
- Account creation and login

### 📤 Resume Upload
- Drag & drop file upload
- PDF validation
- File size checking (max 16MB)
- Duplicate naming support

### 🤖 AI Analysis
- Google Gemini integration
- ATS score (0-100)
- Improvement suggestions
- Professional summary
- Job recommendations

### 📊 Dashboard
- Resume statistics
- Upload history
- ATS score tracking
- Quick actions

### 💾 Database
- Secure user data storage
- Resume content indexing
- Analysis results caching
- Analytics tracking

---

## 🐛 Troubleshooting

### MySQL Connection Error
**Problem:** `Connection refused` or `Can't connect to MySQL`

**Solution:**
```bash
# Check if MySQL is running
mysql -u root -p

# If not, restart
mysql.server restart  # Mac/Linux
net start MySQL80     # Windows
```

### Missing Dependencies
**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### API Key Error
**Problem:** `Error calling Gemini API` or `Invalid API key`

**Solution:**
1. Verify API key at: https://makersuite.google.com/app/apikey
2. Check `.env` file has correct key
3. Ensure no extra spaces in key
4. Key should start with `AIza...`

### Port Already in Use
**Problem:** `Address already in use`

**Solution:**
```bash
# Change port in app.py
# Change: app.run(port=5000)
# To: app.run(port=5001)
```

### Database Not Found
**Problem:** `Database ai_resume_builder doesn't exist`

**Solution:**
```bash
# Run schema script again
mysql -u root -p < database/schema.sql
```

---

## 📱 Testing the Application

### Create Test Account
1. Email: test@example.com
2. Password: TestPass123

### Test Resume
Use any PDF file, or create a simple text document and convert to PDF.

### Check Results
- ATS score should be between 60-85
- Suggestions should be relevant
- Job recommendations should match skills

---

## 🚀 Deployment (Optional)

### Deploy to Heroku

```bash
# Install Heroku CLI
# Then:
heroku login
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere

1. Go to: https://www.pythonanywhere.com
2. Create account
3. Upload files
4. Configure MySQL connection
5. Deploy!

---

## 📚 File Descriptions

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application, route registration |
| `config/settings.py` | Configuration for different environments |
| `database/db_helper.py` | All database query functions |
| `utils/ai_analyzer.py` | Gemini AI integration |
| `utils/pdf_handler.py` | PDF text extraction |
| `utils/validators.py` | Input validation functions |
| `static/css/style.css` | Complete styling |
| `static/js/main.js` | JavaScript utilities |

### Routes

| Route | Purpose |
|-------|---------|
| `/` | Home page |
| `/auth/signup` | User registration |
| `/auth/login` | User login |
| `/auth/logout` | User logout |
| `/resume/upload` | Upload resume |
| `/resume/analyze/<id>` | View analysis |
| `/dashboard/` | Main dashboard |
| `/dashboard/my-resumes` | Resume list |

---

## 🎓 Learning Resources

### Flask
- Official Docs: https://flask.palletsprojects.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Flask-Login: https://flask-login.readthedocs.io/

### MySQL
- Tutorial: https://www.w3schools.com/mysql/
- Workbench: https://www.mysql.com/products/workbench/

### Google Gemini AI
- Documentation: https://ai.google.dev/
- API Reference: https://ai.google.dev/docs

### Bootstrap
- Framework: https://getbootstrap.com/
- Components: https://getbootstrap.com/docs/5.0/components/

---

## 📞 Need Help?

### Common Issues & Fixes

1. **Application won't start**
   - Ensure MySQL is running
   - Check .env file exists and has correct values
   - Verify all dependencies installed

2. **Database errors**
   - Check MySQL connection settings
   - Run schema.sql again
   - Verify database name is correct

3. **AI not working**
   - Verify Gemini API key
   - Check internet connection
   - Review API usage at Google Console

4. **File upload failing**
   - Check file is valid PDF
   - Ensure file < 16MB
   - Check file permissions

---

## ✨ Next Steps

1. ✅ **Setup Complete** - You're ready to go!
2. 📝 **Test Features** - Try uploading a resume
3. 🎨 **Customize** - Modify colors, text, features
4. 📦 **Deploy** - Share with others
5. 🚀 **Enhance** - Add more features

---

## 📄 License

This project is open source. Feel free to modify and use!

---

## 🎉 You're All Set!

Your AI Resume Builder is ready to use. Start by running:

```bash
python app.py
```

Then visit: http://localhost:5000

**Happy Resume Building!** 🚀

---

### Need More Help?
- Check README.md for detailed documentation
- Review code comments in source files
- Check troubleshooting section above

**Last Updated:** June 2024
