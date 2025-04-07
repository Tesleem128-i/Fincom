import sqlite3

def add_columns_to_database():
    # Connect to the database
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    try:
        # Add 'number_of_workers' column to the 'users' table if it doesn't exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'number_of_workers' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN number_of_workers INTEGER DEFAULT 0")
            print("Added 'number_of_workers' column to 'users' table.")

        # Add 'email' column to the 'workers' table if it doesn't exist
        cursor.execute("PRAGMA table_info(workers)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'email' not in columns:
            cursor.execute("ALTER TABLE workers ADD COLUMN email TEXT")
            print("Added 'email' column to 'workers' table.")

        # Add 'status' column to the 'workers' table if it doesn't exist
        if 'status' not in columns:
            cursor.execute("ALTER TABLE workers ADD COLUMN status TEXT DEFAULT 'Pending'")
            print("Added 'status' column to 'workers' table.")

        conn.commit()
        print("Database schema updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while updating the database schema: {e}")
    finally:
        cursor.close()
        conn.close()

# Run the function to update the database schema
add_columns_to_database()