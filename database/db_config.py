import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """PostgreSQL database configuration and connection handler"""
    
    def __init__(self):
        # Try environment variables from Render, fall back to .env
        self.host = os.getenv('DB_HOST') or os.getenv('POSTGRES_HOST', 'localhost')
        self.user = os.getenv('DB_USER') or os.getenv('POSTGRES_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD') or os.getenv('POSTGRES_PASSWORD', '')
        self.database = os.getenv('DB_NAME') or os.getenv('POSTGRES_DB', 'ai_resume_builder')
        self.port = os.getenv('DB_PORT') or os.getenv('POSTGRES_PORT', '5432')
        
        print(f"🔗 Database Config:")
        print(f"   Host: {self.host}")
        print(f"   Database: {self.database}")
        print(f"   User: {self.user}")
    
    def get_connection(self):
        """Create and return PostgreSQL connection"""
        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return connection
        except Error as e:
            print(f"❌ Error connecting to PostgreSQL: {e}")
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