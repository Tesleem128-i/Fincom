import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL command to add a new column 'profession' to the 'users' table
try:
    cursor.execute("ALTER TABLE users ADD COLUMN profession TEXT;")
    print("Column 'profession' added successfully.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()