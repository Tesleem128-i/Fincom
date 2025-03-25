import sqlite3

def create_connections_table():
    # Connect to the SQLite database (replace with your actual database name)
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    # Create the connections table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER NOT NULL,
            user2_id INTEGER NOT NULL,
            FOREIGN KEY (user1_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (user2_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user1_id, user2_id)  -- Prevent duplicate connections
        );
    """)

    conn.commit()  # Save changes
    conn.close()   # Close connection
    print("Connections table created successfully.")

# Call the function to create the table
create_connections_table()