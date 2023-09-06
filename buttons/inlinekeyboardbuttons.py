from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict


def create_inline_keyboard(btns: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard from a list of button dictionaries.
    Each button dictionary should have 'text' and 'data' keys.
    Returns an InlineKeyboardMarkup object.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=btn["text"], callback_data=btn["data"]) for btn in btns]
    keyboard.add(*buttons)
    return keyboard


def get_group_link_button(link: str) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard with a single button to join a group.
    Takes a link parameter as a string and returns an InlineKeyboardMarkup object.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    group_link_button = InlineKeyboardButton(text="Join Group", url=link)
    keyboard.add(group_link_button)
    return keyboard


def inlinekeyboardbuttonlinks(buttons: List[dict]) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard with buttons containing links.

    Parameters:
    buttons (List[dict]): A list of dictionaries where each dictionary represents a button.
                          Each dictionary should have "text" and "link" keys.

    Returns:
    InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    if not isinstance(buttons, list):
        raise ValueError("The 'buttons' parameter should be a list.")

    keyboard = InlineKeyboardMarkup(row_width=2)

    for btn in buttons:
        if not isinstance(btn, dict):
            raise ValueError("Each element in 'buttons' should be a dictionary.")
        if "text" not in btn or "link" not in btn:
            raise ValueError("Each button dictionary should have 'text' and 'link' keys.")
            
        text = btn["text"]
        link = btn["link"]
        button = InlineKeyboardButton(text=text, url=link)
        keyboard.add(button)

    return keyboard

