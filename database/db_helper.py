from psycopg2 import Error
from database.db_config import db_config
from werkzeug.security import generate_password_hash, check_password_hash

class DatabaseHelper:
    """Helper class for database operations"""
    
    @staticmethod
    def fetch_one(query, params=None):
        """Fetch a single row"""
        connection = db_config.get_connection()
        if connection is None:
            return None
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            row = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return row
        except Error as e:
            print(f"Database error: {e}")
            return None
    
    @staticmethod
    def fetch_all(query, params=None):
        """Fetch all rows"""
        connection = db_config.get_connection()
        if connection is None:
            return []
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return rows
        except Error as e:
            print(f"Database error: {e}")
            return []
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute INSERT, UPDATE, DELETE queries"""
        connection = db_config.get_connection()
        if connection is None:
            return False
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False
    
    @staticmethod
    def execute_query_with_id(query, params=None):
        """Execute INSERT and return the new ID"""
        connection = db_config.get_connection()
        if connection is None:
            return None
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            
            # Get the last inserted ID for PostgreSQL
            cursor.execute("SELECT LASTVAL()")
            last_id = cursor.fetchone()[0]
            
            cursor.close()
            connection.close()
            
            return last_id
        except Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return None

# ============ AUTH FUNCTIONS ============

def register_user(username, email, password):
    """Register a new user"""
    hashed_password = generate_password_hash(password)
    query = """
    INSERT INTO users (username, email, password)
    VALUES (%s, %s, %s)
    """
    return DatabaseHelper.execute_query_with_id(query, (username, email, hashed_password))

def login_user(email, password):
    """Verify user login"""
    user = get_user_by_email(email)
    if user and check_password_hash(user[3], password):  # user[3] is password
        return user
    return None

def get_user_by_id(user_id):
    """Get user by ID"""
    query = "SELECT id, username, email, password FROM users WHERE id = %s"
    return DatabaseHelper.fetch_one(query, (user_id,))

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT id, username, email, password FROM users WHERE email = %s"
    return DatabaseHelper.fetch_one(query, (email,))

def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT id, username, email FROM users WHERE username = %s"
    return DatabaseHelper.fetch_one(query, (username,))

def create_user(username, email, password):
    """Create new user (alias for register_user)"""
    return register_user(username, email, password)

def update_user_password(user_id, new_password):
    """Update user password"""
    hashed_password = generate_password_hash(new_password)
    query = "UPDATE users SET password = %s WHERE id = %s"
    return DatabaseHelper.execute_query(query, (hashed_password, user_id))

def delete_user(user_id):
    """Delete user account"""
    query = "DELETE FROM users WHERE id = %s"
    return DatabaseHelper.execute_query(query, (user_id,))

# ============ RESUME FUNCTIONS ============

def save_resume(user_id, file_name, content):
    """Save resume"""
    query = """
    INSERT INTO resumes (user_id, file_name, original_content)
    VALUES (%s, %s, %s)
    """
    return DatabaseHelper.execute_query_with_id(query, (user_id, file_name, content))

def get_resume(resume_id, user_id):
    """Get resume by ID"""
    query = """
    SELECT id, user_id, file_name, original_content, ats_score, 
           professional_summary, ai_suggestions, job_recommendations, uploaded_at
    FROM resumes WHERE id = %s AND user_id = %s
    """
    return DatabaseHelper.fetch_one(query, (resume_id, user_id))

def get_user_resumes(user_id):
    """Get all user resumes"""
    query = """
    SELECT id, user_id, file_name, original_content, ats_score, 
           professional_summary, ai_suggestions, job_recommendations, uploaded_at
    FROM resumes WHERE user_id = %s ORDER BY uploaded_at DESC
    """
    return DatabaseHelper.fetch_all(query, (user_id,))

def save_resume_analysis(resume_id, user_id, ats_score, summary, suggestions, jobs):
    """Save resume analysis"""
    query = """
    UPDATE resumes 
    SET ats_score = %s, professional_summary = %s, ai_suggestions = %s, job_recommendations = %s
    WHERE id = %s AND user_id = %s
    """
    return DatabaseHelper.execute_query(query, (ats_score, summary, suggestions, jobs, resume_id, user_id))

def delete_resume(resume_id, user_id):
    """Delete resume"""
    query = "DELETE FROM resumes WHERE id = %s AND user_id = %s"
    return DatabaseHelper.execute_query(query, (resume_id, user_id))

# ============ COVER LETTER FUNCTIONS ============

def save_cover_letter(user_id, resume_id, job_title, company_name, content):
    """Save cover letter"""
    query = """
    INSERT INTO cover_letters (user_id, resume_id, job_title, company_name, content)
    VALUES (%s, %s, %s, %s, %s)
    """
    return DatabaseHelper.execute_query_with_id(query, (user_id, resume_id, job_title, company_name, content))

def get_cover_letters(user_id):
    """Get user's cover letters"""
    query = "SELECT * FROM cover_letters WHERE user_id = %s ORDER BY created_at DESC"
    return DatabaseHelper.fetch_all(query, (user_id,))

# ============ INTERVIEW PREP FUNCTIONS ============

def save_interview_prep(user_id, resume_id, job_title, company_name, questions, tips, answers):
    """Save interview prep"""
    query = """
    INSERT INTO interview_prep (user_id, resume_id, job_title, company_name, questions, tips, answers)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    return DatabaseHelper.execute_query_with_id(query, (user_id, resume_id, job_title, company_name, questions, tips, answers))

def get_interview_preps(user_id):
    """Get user's interview preps"""
    query = "SELECT * FROM interview_prep WHERE user_id = %s ORDER BY created_at DESC"
    return DatabaseHelper.fetch_all(query, (user_id,))

# ============ SUBSCRIPTION FUNCTIONS ============

def save_subscription(email):
    """Save subscription email"""
    query = "INSERT INTO subscriptions (email) VALUES (%s)"
    return DatabaseHelper.execute_query(query, (email,))