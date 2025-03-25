import os
import sqlite3

def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    # Define the path to the database inside the FINCOM folder
    db_path = os.path.join(os.path.dirname(__file__), "mydatabase.db")
    conn = sqlite3.connect(db_path)  # Use the full path to the database file
    cursor = conn.cursor()

    # Create the `users` table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        fullname TEXT,
        profession TEXT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        nationality TEXT,
        customer_type TEXT,
        profit REAL DEFAULT 0,
        total_income REAL DEFAULT 0,
        total_expenses REAL DEFAULT 0,
        cash_balance REAL DEFAULT 0,
        card_balance REAL DEFAULT 0
    )
    """)

    # Create the `transactions` table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        type TEXT,
        account TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        quantity REAL,
        transaction_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Create the `posts` table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        media_filename TEXT,
        media_type TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create the `responses` table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts (id)
    )
    """)

    conn.commit()  # Save changes
    conn.close()  # Close the connection
    print(f"Database initialized successfully at {db_path}.")

# Call the database initialization function when the app starts
if __name__ == '__main__':
    initialize_database()  # Initialize the database