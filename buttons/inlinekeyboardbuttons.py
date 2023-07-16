"""
buttons inline
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_book(book_id, user_id):
    button = InlineKeyboardButton(text='Click me!', callback_data='button_clicked')

    keyboard = InlineKeyboardMarkup().add(button)
