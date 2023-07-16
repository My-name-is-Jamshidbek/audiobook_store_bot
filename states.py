"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin_state(StatesGroup):
    """
    main state
    """
    main_menu = State()
    book_type = State()

    book_main_menu = State()
    premium_books = State()
    free_books = State()
    book_delete = State()

    premium_book_add_name = State()
    premium_book_add_description = State()
    premium_book_add_audio = State()
    premium_book_add_file = State()
    premium_book_add_price = State()

    free_book_add_name = State()
    free_book_add_description = State()
    free_book_add_audio = State()
    free_book_add_file = State()
    free_book_add_price = State()

    free_book_delete = State()
    free_book_main_menu = State()

    contact_us = State()
    contact_us_change = State()


class User_state(StatesGroup):
    """
    main state
    """

    # for registration
    register = State()
    fullname = State()
    phone_number = State()
    main_menu = State()
    audiobook_type = State()
    free_book_main_menu = State()
    free_books = State()
    premium_book_main_menu = State()
    premium_books = State()
    search_books = State()
