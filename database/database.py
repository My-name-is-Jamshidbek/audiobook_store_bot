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
    c.execute('''CREATE TABLE IF NOT EXISTS free_books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_name TEXT NOT NULL,
                 audiobook_address TEXT NOT NULL,
                 book_description TEXT NOT NULL,
                 book_photo TEXT NOT NULL)''')


    # Create the book table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS premium_books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_name TEXT NOT NULL,
                 audiobook_price TEXT NOT NULL,
                 audiobook_photo TEXT NOT NULL,
                 audiobook_address TEXT NOT NULL,
                 audibook_description TEXT NOT NULL,
                 book_price TEXT NOT NULL,
                 book_photo TEXT NOT NULL,
                 book_address TEXT NOT NULL,
                 book_description TEXT NOT NULL)''')

    conn.commit()
    conn.close()


"""
PREMIUM BOOKS
"""


def get_premium_books():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_name FROM premium_books")
    book_names = [row[0] for row in c.fetchall()]

    conn.close()

    return book_names


def get_premium_book_photo(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_photo FROM premium_books WHERE book_name = ?", (book_name,))
    photo_address = c.fetchone()

    conn.close()

    if photo_address:
        return photo_address[0]
    else:
        return None


def add_premium_book(book_name, audiobook_price, audiobook_photo, audiobook_address, audiobook_description,
                     book_price, book_photo, book_address, book_description):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO premium_books (book_name, audiobook_price, audiobook_photo, audiobook_address, audibook_description, book_price, book_photo, book_address, book_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (book_name, audiobook_price, audiobook_photo, audiobook_address, audiobook_description, book_price, book_photo, book_address, book_description))
    
    conn.commit()
    conn.close()


def get_premium_book_description(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_description FROM premium_books WHERE book_name = ?", (book_name,))
    description = c.fetchone()

    conn.close()

    if description:
        return description[0]
    else:
        return None


def get_premium_book_price(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_price FROM premium_books WHERE book_name = ?", (book_name,))
    price = c.fetchone()

    conn.close()

    if price:
        
        return formatted_price
    else:
        return None
    

def get_premium_book_file(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_address FROM premium_books WHERE book_name = ?", (book_name,))
    audiobook_address = c.fetchone()

    conn.close()

    if audiobook_address:
        return audiobook_address[0]
    else:
        return None
    

def get_premium_audiobook_description(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audibook_description FROM premium_books WHERE book_name = ?", (book_name,))
    audiobook_description = c.fetchone()

    conn.close()

    if audiobook_description:
        return audiobook_description[0]
    else:
        return None


def get_premium_audiobook_price(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_price FROM premium_books WHERE book_name = ?", (book_name,))
    audiobook_price = c.fetchone()

    conn.close()

    if audiobook_price:
        formatted_price = int(audiobook_price[0])
        return formatted_price
    else:
        return None
    

def get_premium_audiobook_photo(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_photo FROM premium_books WHERE book_name = ?", (book_name,))
    audiobook_photo = c.fetchone()

    conn.close()

    if audiobook_photo:
        return audiobook_photo[0]
    else:
        return None
    

def get_premium_audiobook_address(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_address FROM premium_books WHERE book_name = ?", (book_name,))
    audiobook_address = c.fetchone()

    conn.close()

    if audiobook_address:
        return audiobook_address[0]
    else:
        return None
    

def delete_premium_book(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM premium_books WHERE book_name = ?", (book_name,))
    conn.commit()

    conn.close()



def get_premium_book_name_by_id(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_name FROM premium_books WHERE id = ?", (book_id,))
    book_name = c.fetchone()

    conn.close()

    if book_name:
        return book_name[0]
    else:
        return None

def get_premium_book_description_by_id(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_description FROM premium_books WHERE id = ?", (book_id,))
    description = c.fetchone()

    conn.close()

    if description:
        return description[0]
    else:
        return None

def get_premium_book_price_by_id(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_price FROM premium_books WHERE id = ?", (book_id,))
    price = c.fetchone()

    conn.close()

    if price:
        formatted_price = int(price[0])
        return formatted_price
    else:
        return None

def get_premium_audiobook_description_by_id(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_description FROM premium_books WHERE id = ?", (book_id,))
    description = c.fetchone()

    conn.close()

    if description:
        return description[0]
    else:
        return None


def get_premium_audiobook_price_by_id(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_price FROM premium_books WHERE id = ?", (book_id,))
    price = c.fetchone()

    conn.close()

    if price:
        formatted_price = int(price[0])
        return formatted_price
    else:
        return None


def get_premium_book_id(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT id FROM premium_books WHERE book_name = ?", (book_name,))
    book_id = c.fetchone()

    conn.close()

    if book_id:
        return book_id[0]
    else:
        return None
    

def update_premium_book_name(old_name, new_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET book_name = ? WHERE book_name = ?", (new_name, old_name))
    conn.commit()

    conn.close()


def update_premium_audiobook_price(book_name, new_price):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET audiobook_price = ? WHERE book_name = ?", (new_price, book_name))
    conn.commit()

    conn.close()


def update_premium_book_price(book_name, new_price):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET book_price = ? WHERE book_name = ?", (new_price, book_name))
    conn.commit()

    conn.close()


def update_premium_audiobook_photo_type(book_name, audiobook_photo):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET audiobook_photo = ? WHERE book_name = ?", (audiobook_photo, book_name))
    conn.commit()

    conn.close()


def update_premium_book_photo_type(book_name, book_photo):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET book_photo = ? WHERE book_name = ?", (book_photo, book_name))
    conn.commit()

    conn.close()


def update_premium_audiobook_description(book_name, new_description):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET audibook_description = ? WHERE book_name = ?", (new_description, book_name))
    conn.commit()

    conn.close()


def update_premium_book_description(book_name, new_description):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET book_description = ? WHERE book_name = ?", (new_description, book_name))
    conn.commit()

    conn.close()


def update_premium_book_file(book_name, audiobook_address):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET audiobook_address = ? WHERE book_name = ?", (audiobook_address, book_name))
    conn.commit()

    conn.close()


def update_premium_audiobook_audio(book_name, new_audiobook_address):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE premium_books SET audiobook_address = ? WHERE book_name = ?", (new_audiobook_address, book_name))
    conn.commit()

    conn.close()


"""
FREE BOOKS
"""

def get_free_books():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_name FROM free_books")
    book_names = [row[0] for row in c.fetchall()]

    conn.close()

    return book_names


def get_free_book_description(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_description FROM free_books WHERE book_name = ?", (book_name,))
    description = c.fetchone()

    conn.close()

    if description:
        return description[0]
    else:
        return None


def get_free_book_photo(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT book_photo FROM free_books WHERE book_name = ?", (book_name,))
    photo_address = c.fetchone()

    conn.close()

    if photo_address:
        return photo_address[0]
    else:
        return None


def get_free_book_address(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT audiobook_address FROM free_books WHERE book_name = ?", (book_name,))
    address = c.fetchone()

    conn.close()

    if address:
        return address[0]
    else:
        return None


def update_free_book_photo_type(book_name, book_photo):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE free_books SET book_photo = ? WHERE book_name = ?", (book_photo, book_name))
    conn.commit()

    conn.close()


def update_free_book_description(book_name, new_description):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE free_books SET book_description = ? WHERE book_name = ?", (new_description, book_name))
    conn.commit()

    conn.close()


def update_free_book_name(book_name, new_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE free_books SET book_name = ? WHERE book_name = ?", (new_name, book_name))
    conn.commit()

    conn.close()


def update_free_book_address(book_name, new_address):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("UPDATE free_books SET audiobook_address = ? WHERE book_name = ?", (new_address, book_name))
    conn.commit()

    conn.close()


def delete_free_book(book_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("DELETE FROM free_books WHERE book_name = ?", (book_name,))
    conn.commit()

    conn.close()


def add_free_book(book_name, audiobook_address, book_description, book_photo):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO free_books (book_name, audiobook_address, book_description, book_photo) VALUES (?, ?, ?, ?)",
              (book_name, audiobook_address, book_description, book_photo))
    
    conn.commit()
    conn.close()


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


def create_user_premium_book_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the user_premium_books table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS user_premium_books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 tg_id INTEGER NOT NULL,
                 book_id INTEGER NOT NULL,
                 FOREIGN KEY(tg_id) REFERENCES users(tg_id),
                 FOREIGN KEY(book_id) REFERENCES books(id))''')

    conn.commit()
    conn.close()



def add_user_premium_book(tg_id, book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new user_premium_book into the database
    c.execute("INSERT INTO user_premium_books (tg_id, book_id) VALUES (?, ?)", (tg_id, book_id))

    conn.commit()
    conn.close()


def get_user_premium_books(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve premium books for a specific user from the database
    c.execute("SELECT premium_books.* FROM premium_books INNER JOIN user_premium_books ON premium_books.id = user_premium_books.book_id WHERE user_premium_books.tg_id=?", (tg_id,))
    premium_books = c.fetchall()

    conn.close()

    pb = [i[1] for i in premium_books]

    return pb


def create_user_premium_audiobook_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the user_premium_books table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS user_premium_audiobooks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 tg_id INTEGER NOT NULL,
                 book_id INTEGER NOT NULL,
                 FOREIGN KEY(tg_id) REFERENCES users(tg_id),
                 FOREIGN KEY(book_id) REFERENCES books(id))''')

    conn.commit()
    conn.close()

def add_user_premium_audiobook(tg_id, book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new user_premium_book into the database
    c.execute("INSERT INTO user_premium_audiobooks (tg_id, book_id) VALUES (?, ?)", (tg_id, book_id))

    conn.commit()
    conn.close()


def get_user_premium_audiobooks(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve premium books for a specific user from the database
    c.execute("SELECT premium_books.* FROM premium_books INNER JOIN user_premium_audiobooks ON premium_books.id = user_premium_audiobooks.book_id WHERE user_premium_audiobooks.tg_id=?", (tg_id,))
    premium_books = c.fetchall()

    conn.close()

    pb = [i[1] for i in premium_books]

    return pb


def create_database():
    create_book_table()
    create_contact_table()
    create_user_table()
    create_user_premium_book_table()
    create_user_premium_audiobook_table()
