from psycopg2 import Error
from database.db_config import db_config

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
            
            # Convert row to dict
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
            
            # Get the last inserted ID
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