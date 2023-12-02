import sqlite3
from config import DATABASE_NAME


# users functions
def create_starters_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the user table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS starters
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 tg_id TEXT NOT NULL,
                 fullname TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def add_starter_user(tg_id, fullname):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("INSERT INTO starters (tg_id, fullname) VALUES (?, ?)", (tg_id, fullname))

    conn.commit()
    conn.close()
    

def count_starters_users():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM starters")
    count = c.fetchone()[0]

    conn.close()

    return count


def get_all_starters_tg_id():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT tg_id FROM starters")
    tg_ids = [row[0] for row in c.fetchall()]

    conn.close()

    return tg_ids
    
    
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


def all_users_count():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]

    conn.close()

    return count


def get_all_users_tg_id():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("SELECT tg_id FROM users")
    tg_ids = [row[0] for row in c.fetchall()]

    conn.close()

    return tg_ids


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


def create_uc_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the UC table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS uc
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 amount REAL NOT NULL)''')

    conn.commit()
    conn.close()


def update_uc(user_id, new_amount):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Update the UC amount for the specified user
    c.execute("UPDATE uc SET amount = ? WHERE user_id = ?", (new_amount, user_id))

    conn.commit()
    conn.close()


def get_uc(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve UC data for the specified user
    c.execute("SELECT * FROM uc WHERE user_id = ?", (user_id,))
    uc_data = c.fetchone()

    conn.close()

    return int(uc_data[2])


def get_maximum_amount_users(limit):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve users with the maximum "amount" value, limited by the specified limit
    c.execute("SELECT user_id, MAX(amount) FROM invite GROUP BY user_id ORDER BY MAX(amount) DESC LIMIT ?", (limit,))
    maximum_amount_users = c.fetchall()

    conn.close()

    return maximum_amount_users

def get_user_name_by_id(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # user_id'ga mos keladigan foydalanuvchi nomini topadi
    c.execute("SELECT fullname FROM users WHERE tg_id = ?", (user_id,))
    user_name = c.fetchone()

    conn.close()

    return user_name[0] if user_name else None

def add_uc(user_id, amount):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new UC record into the database
    c.execute("INSERT INTO uc (user_id, amount) VALUES (?, ?)", (user_id, amount))

    conn.commit()
    conn.close()

def create_invite_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the invite table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS invite
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 amount REAL NOT NULL)''')

    conn.commit()
    conn.close()


def update_invite(user_id, new_amount):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Update the invite amount for the specified user
    c.execute("UPDATE invite SET amount = ? WHERE user_id = ?", (new_amount, user_id))

    conn.commit()
    conn.close()


def get_invite(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve invite data for the specified user
    c.execute("SELECT * FROM invite WHERE user_id = ?", (user_id,))
    invite_data = c.fetchone()

    conn.close()

    return int(invite_data[2])


def add_invite(user_id, amount):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new invite record into the database
    c.execute("INSERT INTO invite (user_id, amount) VALUES (?, ?)", (user_id, amount))

    conn.commit()
    conn.close()


def create_settings_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the settings table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 value TEXT NOT NULL)''')

    conn.commit()
    conn.close()

# Settings functions

def update_setting(name, value):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Update a setting in the database based on its name
    c.execute("UPDATE settings SET value=? WHERE name=?", (value, name))

    conn.commit()
    conn.close()


def get_setting(name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve a setting from the database based on its name
    c.execute("SELECT value FROM settings WHERE name=?", (name,))
    setting = c.fetchone()

    conn.close()

    if setting:
        return setting[0]
    else:
        return None


def add_setting(name, value):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new setting into the database
    c.execute("INSERT INTO settings (name, value) VALUES (?, ?)", (name, value))

    conn.commit()
    conn.close()


# Channels functions

def create_channels_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the channels table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS channels
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 url TEXT NOT NULL)''')

    conn.commit()
    conn.close()

def add_channel(name, url):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new channel into the database
    c.execute("INSERT INTO channels (name, url) VALUES (?, ?)", (name, url))

    conn.commit()
    conn.close()

def get_all_channels():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve all channels from the database
    c.execute("SELECT name, url FROM channels")
    channels = c.fetchall()

    conn.close()

    return channels


# Delete a channel by name
def delete_channel(name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Delete the channel from the database based on its name
    c.execute("DELETE FROM channels WHERE name=?", (name,))

    conn.commit()
    conn.close()


def get_channels_names():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve all channel names from the database
    c.execute("SELECT name FROM channels")
    channel_names = [row[0] for row in c.fetchall()]

    conn.close()

    return channel_names


def create_uc_price_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the UC table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS uc_prices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 price INTEGER NOT NULL,
                 amount REAL NOT NULL)''')

    conn.commit()
    conn.close()


def get_uc_price(_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve UC data for the specified user
    c.execute("SELECT * FROM uc_prices WHERE id = ?", (_id,))
    uc_data = c.fetchone()

    conn.close()

    return int(uc_data[1])

def get_uc_amount(_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve UC data for the specified user
    c.execute("SELECT * FROM uc_prices WHERE id = ?", (_id,))
    uc_data = c.fetchone()

    conn.close()

    return int(uc_data[2])

def get_uc_prices():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve UC data for the specified user
    c.execute("SELECT * FROM uc_prices")
    uc_data = c.fetchall()

    conn.close()

    return uc_data

def add_uc_price(price, amount):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Insert a new UC record into the database
    c.execute("INSERT INTO uc_prices (price, amount) VALUES (?, ?)", (price, amount))

    conn.commit()
    conn.close()


def delete_uc_price_by_id(_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Delete the UC price record with the specified ID
    c.execute("DELETE FROM uc_prices WHERE id = ?", (_id,))

    conn.commit()
    conn.close()

def create_buy_uc_table():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Create the buy_uc table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS buy_uc
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 thrown_away BOOLEAN NOT NULL,
                 uc_price_id INTEGER NOT NULL,
                 tg_id INTEGER NOT NULL,
                 purchase_date DATE NOT NULL,
                 FOREIGN KEY (uc_price_id) REFERENCES uc_prices(id))''')

    conn.commit()
    conn.close()

import datetime

def buy_uc(uc_price_id, tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Get the current date and time
    purchase_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert a new purchase record into the buy_uc table with thrown_away set to True
    c.execute("INSERT INTO buy_uc (thrown_away, uc_price_id, tg_id, purchase_date) VALUES (?, ?, ?, ?)",
              (False, uc_price_id, tg_id, purchase_date))

    # Commit the transaction and get the ID of the newly inserted record
    conn.commit()
    inserted_id = c.lastrowid

    conn.close()

    return inserted_id

def update_thrown_away_status(purchase_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Update the "thrown_away" status for the specified purchase_id
    c.execute("UPDATE buy_uc SET thrown_away = ? WHERE id = ?", (True, purchase_id))

    conn.commit()
    conn.close()


def get_buy_uc_tg_id(purchase_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the tg_id associated with the specified purchase_id
    c.execute("SELECT tg_id FROM buy_uc WHERE id = ?", (purchase_id,))
    tg_id = c.fetchone()

    conn.close()

    if tg_id:
        return tg_id[0]  # Return the tg_id value
    else:
        return None  # Return None if no matching record is found
    
    
def get_fullname_user_by_tg_id(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the fullname of a user based on their tg_id
    c.execute("SELECT fullname FROM users WHERE tg_id = ?", (tg_id,))
    fullname = c.fetchone()

    conn.close()

    return fullname[0] if fullname else None


def get_uc_amount_by_tg_id(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the UC amount of a user based on their tg_id
    c.execute("SELECT uc.amount FROM uc INNER JOIN users ON uc.user_id = users.id WHERE users.tg_id = ?", (tg_id,))
    uc_amount = c.fetchone()

    conn.close()

    return uc_amount[0] if uc_amount else None


def get_invited_people_by_tg_id(tg_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Retrieve the list of people invited by a user based on their tg_id
    c.execute("SELECT users.fullname FROM users INNER JOIN invite ON users.id = invite.user_id WHERE invite.user_id = (SELECT id FROM users WHERE tg_id = ?)", (tg_id,))
    invited_people = c.fetchall()

    conn.close()

    return [invite[0] for invite in invited_people] if invited_people else []


def create_database():
    create_contact_table()
    create_user_table()
    create_starters_table()
    create_invite_table()
    create_uc_table()
    create_settings_table()
    add_setting("min_release_uc", "5")
    add_setting("add_man_uc", "1")
    add_setting("starter_uc", "5")
    create_channels_table()
    create_uc_price_table()
    create_buy_uc_table()
