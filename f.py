import sqlite3

def create_messages_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # SQL command to create the messages table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        username TEXT NOT NULL UNIQUE,
        receiver_id INTEGER,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'sent',  -- 'sent', 'delivered', 'read'
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    );
    """

    try:
        # Execute the SQL command
        cursor.execute(create_table_query)
        print("Messages table created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_messages_table()