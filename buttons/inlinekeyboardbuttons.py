"""
buttons inline
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inlinekeyboardbutton(btns):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=btn["text"], callback_data=btn["data"]) for btn in btns]
    keyboard.add(*buttons)
    return keyboard
