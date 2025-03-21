import sqlite3

def create_tables():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        fullname TEXT,
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

    # Create transactions table
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

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")