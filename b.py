import sqlite3
conn = get_db_connection()
cursor = conn.cursor()

try:
    cursor.execute("SELECT currency FROM users WHERE id = ?", (user_id,))  # Correct syntax
    user_currency = cursor.fetchone()
    print("Fetched currency:", user_currency)  # Debugging line
finally:
    cursor.close()
    conn.close()
