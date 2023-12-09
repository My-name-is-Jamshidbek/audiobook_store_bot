import sqlite3
from config import DATABASE_NAME


# payment us
def create_payment_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the payment table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS payment_us
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 message TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def insert_payment_message(message):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new payment message into the database
    c.execute("INSERT INTO payment_us (message) VALUES (?)", (message,))

    conn.commit()
    conn.close()


def get_latest_payment_message():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        # Retrieve the latest payment message from the database
        c.execute("SELECT message FROM payment_us")
        result = c.fetchall()

        conn.close()
    except Exception as e:
        return "NO payment"+str(e)
    if result:
        return result[-1][0]  # Return the latest payment message
    else:
        return "NO payment"
