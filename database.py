import sqlite3

def create_database():
    try:
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()

        # Create 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nationality TEXT NOT NULL,
                customer_type TEXT CHECK(customer_type IN ('individual', 'business')) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cash_balance REAL DEFAULT 0.0,
                card_balance REAL DEFAULT 0.0,
                saving_balance REAL DEFAULT 0.0,
                profit REAL DEFAULT 0.0,
                total_expenses REAL DEFAULT 0.0,
                total_income REAL DEFAULT 0.0
            )
        """)
        # Create 'expenses' table if not already created
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                expense_type TEXT NOT NULL,
                account TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                quantity INTEGER NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Create 'income_categories' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # Insert predefined income categories
        income_categories = [
            ('Rental Income',), ('Business Profit',), ('Freelance',),
            ('Investment',), ('Salary',)
        ]
        cursor.executemany("INSERT OR IGNORE INTO income_categories (name) VALUES (?)", income_categories)

        # Create 'expense_categories' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        # Insert predefined expense categories
        expense_categories = [
            ('Entertainment',), ('Transportation',), ('Groceries',),
            ('Utilities',), ('Rent',)
        ]
        cursor.executemany("INSERT OR IGNORE INTO expense_categories (name) VALUES (?)", expense_categories)

        # Create 'transactions' table (linked to 'users' and category tables)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                account TEXT NOT NULL,
                category TEXT NOT NULL,  -- Changed from category_id to category
                description TEXT,
                amount REAL NOT NULL,
                quantity INTEGER NOT NULL,
                total_amount REAL GENERATED ALWAYS AS (amount * quantity) STORED,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

# Call the function to create the database
create_database()

