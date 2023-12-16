"""
data base
"""

import time
import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# from cryptography.fernet import Fernet

from config import *

import sqlite3
from sqlite3 import Connection

if not os.path.exists("database.db"):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    # Create the vooters table
    c.execute("CREATE TABLE vooters (id INTEGER PRIMARY KEY, name TEXT, votes INTEGER)")

    # Create the users table with a foreign key reference to vooters
    c.execute("""
        CREATE TABLE users (
            telegram_id INTEGER PRIMARY KEY,
            vooter_id INTEGER,
            FOREIGN KEY (vooter_id) REFERENCES vooters(id)
        )
    """)
    c.execute(
        "CREATE TABLE channels (id INTEGER PRIMARY KEY, name TEXT, link INTEGER)")

    conn.commit()
    conn.close()

def add_a_vote(name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Check if the voter with the given name exists
    c.execute("SELECT * FROM vooters WHERE name=?", (name,))
    existing_vooter = c.fetchone()

    if existing_vooter:
        # If the vooter exists, increment the votes by 1
        c.execute("UPDATE vooters SET votes = votes + 1 WHERE name=?", (name,))
    else:
        # If the vooter doesn't exist, create a new entry with 1 vote
        c.execute("INSERT INTO vooters (name, votes) VALUES (?, 1)", (name,))

    conn.commit()
    conn.close()

async def users_count():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]

    conn.close()

    return count

def create_channel(name, link):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO channels (name, link) VALUES (?, ?)", (name, link))

    conn.commit()
    conn.close()

def read_channels():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM channels")
    rows = c.fetchall()

    channels = []
    for row in rows:
        channels.append({"id": row[0], "name": row[1], "link": row[2]})

    return channels

def delete_channel(channel_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Delete the channel with the specified ID
    c.execute("DELETE FROM channels WHERE name=?", (channel_name,))

    conn.commit()
    conn.close()

def read_vooters():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM vooters")
    rows = c.fetchall()

    vooters = []
    for row in rows:
        vooters.append({"id": row[0], "name": row[1], "votes": row[2]})

    return vooters

def read_voters():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM vooters")
    rows = c.fetchall()

    vooters = []
    for row in rows:
        vooters.append({"id": row[0], "name": row[1], "votes": row[2]})

    return vooters

def create_vooter(name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO vooters (name, votes) VALUES (?, ?)", (name, 0))

    conn.commit()
    conn.close()

def add_user(telegram_id, voter_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get the vooter ID based on the provided voter_name
    vooter_id = get_voter_id(voter_name)

    # Insert the user into the "users" table
    c.execute("INSERT INTO users (telegram_id, vooter_id) VALUES (?, ?)", (telegram_id, vooter_id))

    conn.commit()
    conn.close()
    
def check_exist_user(telegram_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Check if the user with the given Telegram ID exists
    c.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
    result = c.fetchone()

    conn.close()

    return result is not None
    
def get_voter_id(voter_name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get the vooter ID based on the provided voter_name
    c.execute("SELECT id FROM vooters WHERE name=?", (voter_name,))
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        # Handle the case where the voter name is not found
        return None


def delete_voter(name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM vooters WHERE name=?", (name,))

    conn.commit()
    conn.close()