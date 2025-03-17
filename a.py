import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# Alter table to add currency column
cursor.execute("ALTER TABLE users ADD COLUMN currency TEXT;")

# Commit and close
conn.commit()
conn.close()

print("Column 'currency' added successfully!")
