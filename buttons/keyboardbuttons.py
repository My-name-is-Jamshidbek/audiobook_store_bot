"""
buttons reply
"""
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def keyboardbutton(btns, resize_keyboard = True, row = 1):
    btns = [btns[i:i+row] for i in range(0,len(btns),row)]
    btns = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=resize_keyboard, row_width=row)
    return btns


share_contact_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
share_contact_button.add(KeyboardButton(text="Telefon raqamim 📱", request_contact=True))

