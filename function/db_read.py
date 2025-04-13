import psycopg2
from psycopg2.extras import RealDictCursor
from service.database.db_connect import ConnectDB

# Database connection details
db_params = {
    "dbname": "Smart Report",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

# Initialize database connection
db_connection = ConnectDB(**db_params)
conn = db_connection.connect()

def reconnect():
    """Re-establish database connection if lost."""
    global conn
    conn = db_connection.connect()

def get_all_data_db():
    """Fetch all data from the database"""
    try:
        if conn.closed:
            reconnect()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM batch_data") 
            data = cursor.fetchall()
        return data
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        return []
