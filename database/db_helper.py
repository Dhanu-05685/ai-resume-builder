from database.db_config import db_config
from mysql.connector import Error

class DatabaseHelper:
    """Helper class for database operations"""
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute INSERT, UPDATE, DELETE queries"""
        connection = db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return last_id
        except Error as e:
            print(f"Database error: {e}")
            connection.rollback()
            connection.close()
            return None

    @staticmethod
    def fetch_one(query, params=None):
        """Fetch single row"""
        connection = db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"Database error: {e}")
            connection.close()
            return None

    @staticmethod
    def fetch_all(query, params=None):
        """Fetch multiple rows"""
        connection = db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            return results
        except Error as e:
            print(f"Database error: {e}")
            connection.close()
            return None

    @staticmethod
    def execute_many(query, data_list):
        """Execute multiple queries"""
        connection = db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.executemany(query, data_list)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Database error: {e}")
            connection.rollback()
            connection.close()
            return False

# ============ USER OPERATIONS ============

def create_user(username, email, hashed_password):
    """Create new user"""
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    return DatabaseHelper.execute_query(query, (username, email, hashed_password))

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    return DatabaseHelper.fetch_one(query, (email,))

def get_user_by_id(user_id):
    """Get user by ID"""
    query = "SELECT * FROM users WHERE id = %s"
    return DatabaseHelper.fetch_one(query, (user_id,))

def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    return DatabaseHelper.fetch_one(query, (username,))

# ============ RESUME OPERATIONS ============

def create_resume(user_id, resume_name, content):
    """Create new resume"""
    query = "INSERT INTO resumes (user_id, resume_name, original_content) VALUES (%s, %s, %s)"
    return DatabaseHelper.execute_query(query, (user_id, resume_name, content))

def get_user_resumes(user_id):
    """Get all resumes for user"""
    query = "SELECT * FROM resumes WHERE user_id = %s ORDER BY created_at DESC"
    return DatabaseHelper.fetch_all(query, (user_id,))

def get_resume(resume_id, user_id):
    """Get specific resume"""
    query = "SELECT * FROM resumes WHERE id = %s AND user_id = %s"
    return DatabaseHelper.fetch_one(query, (resume_id, user_id))

def update_resume_analysis(resume_id, ats_score, suggestions, summary, jobs):
    """Update resume with AI analysis"""
    query = """UPDATE resumes SET ats_score = %s, ai_suggestions = %s, 
               professional_summary = %s, job_recommendations = %s WHERE id = %s"""
    return DatabaseHelper.execute_query(query, (ats_score, suggestions, summary, jobs, resume_id))

def delete_resume(resume_id, user_id):
    """Delete resume"""
    query = "DELETE FROM resumes WHERE id = %s AND user_id = %s"
    return DatabaseHelper.execute_query(query, (resume_id, user_id))

def get_resume_count(user_id):
    """Get count of resumes for user"""
    query = "SELECT COUNT(*) as count FROM resumes WHERE user_id = %s"
    result = DatabaseHelper.fetch_one(query, (user_id,))
    return result['count'] if result else 0

def delete_resume(resume_id, user_id):
    """Delete a resume by ID"""
    try:
        from database.db_helper import DatabaseHelper
        
        # First verify the resume belongs to this user
        query = "SELECT id FROM resumes WHERE id = %s AND user_id = %s"
        result = DatabaseHelper.fetch_one(query, (resume_id, user_id))
        
        if not result:
            return False
        
        # Delete the resume
        delete_query = "DELETE FROM resumes WHERE id = %s AND user_id = %s"
        DatabaseHelper.execute_query(delete_query, (resume_id, user_id))
        
        return True
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return False
