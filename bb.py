import sqlite3

def add_column():
    try:
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
    
        cursor.execute("ALTER TABLE transactions ADD COLUMN time DATETIME;")
        
        conn.commit()
        conn.close()
        print("Column 'time' added successfully!")
    except sqlite3.Error as e:
        print(f"Error modifying database: {e}")

add_column()
def update_existing_records():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    
    # Update existing rows to set a timestamp
    cursor.execute("UPDATE transactions SET time = DATETIME('now') WHERE time IS NULL;")
    
    conn.commit()
    conn.close()
    print("Updated existing records with timestamps.")

update_existing_records()
