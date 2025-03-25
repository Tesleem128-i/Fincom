import sqlite3
import os

# Define the database path inside the FINCOM folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'video_db.db')

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def create_posts_table():
    """Create the posts table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        media_filename TEXT, 
        media_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Posts table created successfully.")
    except sqlite3.Error as e:
        print("An error occurred while creating the posts table:", e)
    finally:
        conn.close()

def create_responses_table():
    """Create the responses table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        username TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    '''
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Responses table created successfully.")
    except sqlite3.Error as e:
        print("An error occurred while creating the responses table:", e)
    finally:
        conn.close()

def initialize_database():
    """Initialize the database by creating all necessary tables."""
    print(f"Initializing database at {DB_PATH}...")
    create_posts_table()
    create_responses_table()
    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()