"""
buttons inline
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inlinekeyboardbutton(btns):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=btn["text"], callback_data=btn["data"]) for btn in btns]
    keyboard.add(*buttons)
    return keyboard


def get_group_link_button(link):
    keyboard = InlineKeyboardMarkup(row_width=1)
    group_link_button = InlineKeyboardButton(text="Guruhga qo'shilish", url=link)
    keyboard.add(group_link_button)
    return keyboard