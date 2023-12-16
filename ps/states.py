"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    """
    userlar uchun asosiy holat
    """
    login = State()
    vote = State()
    number = State()
    
class Admin(StatesGroup):
    """
    userlar uchun asosiy holat
    """
    main = State()
    channels_menu = State()
    channels_create = State()
    channels_delete = State()
    channels_create1 = State()
    voters_menu = State()
    voters_create = State()
    voters_delete = State()
    voters_create1 = State()