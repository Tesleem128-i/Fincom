import sqlite3

# Connect to the new database 'video_db.db'
conn = sqlite3.connect('video_db.db')
cursor = conn.cursor()

# Create the posts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        media_filename TEXT, 
        media_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database 'video_db.db' and table 'posts' created successfully!")


import sqlite3

def connect_db():
    # Replace 'your_database.db' with the path to your SQLite database file
    return sqlite3.connect('video_db.db')

def create_responses_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL command to create the responses table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        username TEXT,
        content TEXT,
        timestamp DATETIME,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    );
    '''
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("Responses table created successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    create_responses_table()