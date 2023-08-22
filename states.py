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


    admin_book_add_name = State()

    admin_book_add_photo = State()
    admin_book_add_description = State()
    admin_book_add_price = State()
    admin_book_add_file = State()
    
    admin_audiobook_add_photo = State()
    admin_audiobook_add_description = State()
    admin_audiobook_add_price = State()
    admin_audiobook_add_audio = State()
    
    
    premium_book_update_main_menu = State()
    premium_book_update_name = State()
    premium_audiobook_update_price = State()
    premium_audiobook_update_photo = State()
    premium_audiobook_update_about = State()
    premium_book_update_price = State()
    premium_book_update_photo = State()
    premium_book_update_file = State()
    premium_book_update_about = State()
    premium_audiobook_update_audio = State()
    premium_book_audio = State()

    free_book_add_name = State()
    free_book_add_description = State()
    free_book_add_group = State()
    free_book_add_photo = State()

    free_book_delete = State()
    free_book_main_menu = State()

    free_book_update_name = State()
    free_book_update_description = State()
    free_book_update_group = State()
    free_book_update_photo = State()
    admin_free_book_update_main_menu = State()
    audiobooks = State()
    contact_us = State()
    contact_us_change = State()
    
    give_book_type = State()
    give_book_user = State()


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
    premium_books_audio = State()

    book_type = State()
    
    search_books = State()
    audiobooks = State()

    user_free_book_download = State()
    download_premium_book = State()

