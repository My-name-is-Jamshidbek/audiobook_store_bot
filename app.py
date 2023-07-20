"""
app file
"""
from aiogram.types import ContentType as ct

from apps.admin import *
from apps.user import *
from loader import dp

from apps.login import cmd_start, fullname, phone_number, register
from apps.user import user_main_menu
from states import User_state, Admin_state


# cmd start
dp.register_message_handler(cmd_start, content_types=[ct.TEXT])

"""
ADMIN APPS
"""

# Admin main menu
dp.register_message_handler(admin_main_menu, content_types=[ct.TEXT], state=Admin_state.main_menu)

# Admin book type
dp.register_message_handler(admin_book_type, content_types=[ct.TEXT], state=Admin_state.book_type)

# Admin premium books
dp.register_message_handler(admin_premium_books, content_types=[ct.TEXT], state=Admin_state.premium_books)

# Admin book add name
dp.register_message_handler(admin_book_add_name, content_types=[ct.TEXT], state=Admin_state.premium_book_add_name)

# Admin book add description
dp.register_message_handler(admin_book_add_description, content_types=[ct.TEXT],
                            state=Admin_state.premium_book_add_description)

# Admin book add audio
dp.register_message_handler(admin_book_add_audio, content_types=[ct.AUDIO, ct.TEXT], state=Admin_state.premium_book_add_audio)

# Admin book add file
dp.register_message_handler(admin_book_add_file, content_types=[ct.DOCUMENT, ct.TEXT], state=Admin_state.premium_book_add_file)

# Admin book add price
dp.register_message_handler(admin_book_add_price, content_types=[ct.TEXT], state=Admin_state.premium_book_add_price)

# Admin book main menu
dp.register_message_handler(admin_book_main_menu, content_types=[ct.TEXT], state=Admin_state.book_main_menu)

# Admin book delete
dp.register_message_handler(admin_book_delete, content_types=[ct.TEXT], state=Admin_state.book_delete)

# Admin free books
dp.register_message_handler(admin_free_books, content_types=[ct.TEXT], state=Admin_state.free_books)

# Admin free book add name
dp.register_message_handler(admin_free_book_add_name, content_types=[ct.TEXT], state=Admin_state.free_book_add_name)

# Admin free book add description
dp.register_message_handler(admin_free_book_add_description, content_types=[ct.TEXT], state=Admin_state.free_book_add_description)

# Admin free book add audio
dp.register_message_handler(admin_free_book_add_audio, content_types=[ct.AUDIO, ct.TEXT], state=Admin_state.free_book_add_audio)

# Admin free book add file
dp.register_message_handler(admin_free_book_add_file, content_types=[ct.DOCUMENT, ct.TEXT], state=Admin_state.free_book_add_file)

# Admin freee book main menu
dp.register_message_handler(admin_free_book_main_menu, content_types=[ct.TEXT], state=Admin_state.free_book_main_menu)

# Admin free book delete
dp.register_message_handler(admin_free_book_delete, content_types=[ct.TEXT], state=Admin_state.free_book_delete)

# Admin contact us
dp.register_message_handler(admin_contact_us, content_types=[ct.TEXT], state=Admin_state.contact_us)

# Admin contact us change
dp.register_message_handler(admin_contact_us_change, content_types=[ct.TEXT], state=Admin_state.contact_us_change)

"""
USER APPS
"""

# Register

dp.register_message_handler(fullname, content_types=[ct.TEXT], state=User_state.fullname)

dp.register_message_handler(phone_number, content_types=[ct.TEXT, ct.CONTACT], state=User_state.phone_number)

dp.register_message_handler(user_main_menu, content_types=[ct.TEXT], state=User_state.main_menu)

dp.register_message_handler(user_audiobook_type, content_types=[ct.TEXT], state=User_state.audiobook_type)

dp.register_message_handler(user_free_book_main_menu, content_types=[ct.TEXT], state=User_state.free_book_main_menu)

dp.register_message_handler(user_free_books, content_types=[ct.TEXT], state=User_state.free_books)

dp.register_message_handler(user_premium_book_main_menu, content_types=[ct.TEXT], state=User_state.premium_book_main_menu)

dp.register_message_handler(user_premium_books, content_types=[ct.TEXT], state=User_state.premium_books)

dp.register_message_handler(register, content_types=[ct.TEXT], state=User_state.register)

dp.register_message_handler(search_books, content_types=[ct.TEXT], state=User_state.search_books)
