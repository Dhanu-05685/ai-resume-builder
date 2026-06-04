import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration and connection handler"""
    
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')
        self.database = os.getenv('MYSQL_DATABASE', 'ai_resume_builder')
        self.port = int(os.getenv('MYSQL_PORT', 3306))

    def get_connection(self):
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=False
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def test_connection(self):
        """Test if connection is working"""
        connection = self.get_connection()
        if connection is None:
            print("❌ Connection FAILED")
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            print("✅ Connection SUCCESSFUL!")
            return True
        except Error as e:
            print(f"❌ Connection test failed: {e}")
            return False

# Create global config instance
db_config = DatabaseConfig()
