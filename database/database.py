import sqlite3
from config import DATABASE_NAME


# users functions
def create_user_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the user table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 tg_id TEXT NOT NULL,
                 fullname TEXT NOT NULL,
                 phone_number TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def add_user(tg_id, fullname, phone_number):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new user into the database
    c.execute("INSERT INTO users (tg_id, fullname, phone_number) VALUES (?, ?, ?)", (tg_id, fullname, phone_number))

    conn.commit()
    conn.close()


def get_user(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve a user from the database based on their ID
    c.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
    user = c.fetchone()

    conn.close()

    return user


def user_exists(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve a user from the database based on their tg_id
    c.execute("SELECT 1 FROM users WHERE tg_id=?", (tg_id,))
    user_exist = c.fetchone() is not None

    conn.close()
    return user_exist


# books functions
def create_book_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the book table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_name TEXT NOT NULL,
                 audiobook_address TEXT NOT NULL,
                 file_address TEXT NOT NULL,
                 premium_book INTEGER NOT NULL,
                 book_description TEXT NOT NULL,
                 book_price REAL NOT NULL)''')

    conn.commit()
    conn.close()


def add_book(book_name, audiobook_address, file_address, premium_book, book_description, book_price):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new book into the database
    c.execute("INSERT INTO books (book_name, audiobook_address, file_address, premium_book, book_description, "
              "book_price) VALUES (?, ?, ?, ?, ?, ?)",
              (book_name, audiobook_address, file_address, premium_book, book_description, book_price))

    conn.commit()
    conn.close()


def update_book(book_id, book_name, audiobook_address, file_address, premium_book, book_description, book_price):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Update a book's information in the database
    c.execute("UPDATE books SET book_name=?, audiobook_address=?, file_address=?, premium_book=?, book_description=?, "
              "book_price=? WHERE id=?",
              (book_name, audiobook_address, file_address, premium_book, book_description, book_price, book_id))

    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Delete a book from the database
    c.execute("DELETE FROM books WHERE id=?", (book_id,))

    conn.commit()
    conn.close()


def get_book(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve a book from the database based on its ID
    c.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = c.fetchone()

    conn.close()

    return book


def get_premium_books():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve premium books from the database
    c.execute("SELECT * FROM books WHERE premium_book=1")
    premium_books = c.fetchall()

    conn.close()

    if len(premium_books) < 1:
        premium_books = []

    return [book[1] for book in premium_books]


def get_free_books():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve premium books from the database
    c.execute("SELECT * FROM books WHERE premium_book=0")
    free_books = c.fetchall()

    conn.close()

    if len(free_books) < 1:
        free_books = []

    return [book[1] for book in free_books]


def get_premium_book_description(name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the book description of a premium book by name
    c.execute("SELECT book_description FROM books WHERE premium_book=1 AND book_name=?", (name,))
    book_description = c.fetchone()

    conn.close()

    return book_description[0] if book_description else None


def delete_premium_book(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Delete a premium book by name
    c.execute("DELETE FROM books WHERE premium_book=1 AND book_name=?", (book_name,))

    conn.commit()
    conn.close()


def get_premium_audiobook_path(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the audiobook address of a premium book by name
    c.execute("SELECT audiobook_address FROM books WHERE premium_book=1 AND book_name=?", (book_name,))
    audiobook_address = c.fetchone()

    conn.close()

    return audiobook_address[0] if audiobook_address else None


def get_premium_book_file_address_path(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the file address of a premium book by name
    c.execute("SELECT file_address FROM books WHERE premium_book=1 AND book_name=?", (book_name,))
    file_address = c.fetchone()

    conn.close()

    return file_address[0] if file_address else None


def get_free_book_description(name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the book description from the database based on the name
    c.execute("SELECT book_description FROM books WHERE book_name = ? AND premium_book = 0", (name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the book description
    else:
        return None  # Book not found


def delete_free_book(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Delete the free book from the database
    c.execute("DELETE FROM books WHERE book_name = ? AND premium_book = 0", (book_name,))

    conn.commit()
    conn.close()


def get_free_book_file_address(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the file address from the database based on the book name
    c.execute("SELECT file_address FROM books WHERE book_name = ? AND premium_book = 0", (book_name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the file address
    else:
        return None  # Book not found or no file address available


def get_free_audiobook_path(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the audiobook address from the database based on the book name
    c.execute("SELECT audiobook_address FROM books WHERE book_name = ? AND premium_book = 0", (book_name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the audiobook path
    else:
        return None  # Book not found or no audiobook path available


def get_premium_book_price(name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the price from the database based on the book name
    c.execute("SELECT book_price FROM books WHERE book_name = ? AND premium_book = 1", (name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the book price
    else:
        return None  # Book not found or no price available


# contact us
def create_contact_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the contact table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS contact_us
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 message TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def insert_contact_message(message):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new contact message into the database
    c.execute("INSERT INTO contact_us (message) VALUES (?)", (message,))

    conn.commit()
    conn.close()


def get_latest_contact_message():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    try:
        # Retrieve the latest contact message from the database
        c.execute("SELECT message FROM contact_us ORDER BY id DESC LIMIT 1")
        result = c.fetchone()

        conn.close()
    except:
        return "NO CONTACT"
    if result:
        return result[0]  # Return the latest contact message
    else:
        return "NO CONTACT"


def search_book(keyword):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Search for books based on the keyword in book name or description
    c.execute("SELECT * FROM books WHERE book_name LIKE ? OR book_description LIKE ?", ('%{}%'.format(keyword), '%{}%'.format(keyword)))
    books = c.fetchall()

    conn.close()

    return books
