"""
app file
"""
from aiogram.types import ContentType as ct, PreCheckoutQuery

from apps.admin import *
from apps.user import *
from loader import dp

from apps.login import cmd_start, register, phone_number
# from apps.payment_helper import on_callback_query
# from apps.admin_premium_book_update import premium_book_update_name, premium_audiobook_update_price, premium_audiobook_update_photo, premium_audiobook_update_about, premium_book_update_price, premium_book_update_photo, premium_book_update_file, premium_book_update_about, premium_audiobook_update_audio
from states import User_state, Admin_state

# cmd start
dp.register_message_handler(cmd_start, commands=['start'])

# Register
dp.register_message_handler(register, content_types=[ct.TEXT], state=User_state.register)

dp.register_message_handler(phone_number, content_types=[ct.TEXT, ct.CONTACT], state=User_state.phone_number)

"""
PAYMENT
"""

# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_check_query(pre_checkout_q: PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# @dp.message_handler(content_types=[ct.SUCCESSFUL_PAYMENT])
# async def succesfull_pay(m: m):
#     try:
#         if m.successful_payment.invoice_payload.split("_")[1] == "e":
#             add_user_premium_book(tg_id=m.from_user.id, book_id=get_premium_book_id(m.successful_payment.invoice_payload.split("_")[0]))
#             await m.answer(f"{m.successful_payment.invoice_payload} nomli kitobning elektron versiyasi uchun {m.successful_payment.total_amount // 100} {m.successful_payment.currency} to'lov qilindi kitobni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin.", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
#         elif m.successful_payment.invoice_payload.split("_")[1] == "a":
#             add_user_premium_audiobook(tg_id=m.from_user.id, book_id=get_premium_book_id(m.successful_payment.invoice_payload.split("_")[0]))
#             await m.answer(f"{m.successful_payment.invoice_payload} nomli kitobning to'liq uchun {m.successful_payment.total_amount // 100} {m.successful_payment.currency} to'lov qilindi kitobni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin.", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
#     except:
#         await m.answer(f"Tizimda xatolik yuzaga keldi iltimos admin bilan bog'laning", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
#     await User_state.main_menu.set()


"""
ADMIN APPS
"""
# Admin main menu
dp.register_message_handler(admin_main_menu, content_types=[ct.TEXT], state=Admin_state.main_menu)

# Admin contact us
dp.register_message_handler(admin_contact_us, content_types=[ct.TEXT], state=Admin_state.contact_us)

# Admin contact us change
dp.register_message_handler(admin_contact_us_change, content_types=[ct.TEXT], state=Admin_state.contact_us_change)

# AD

dp.register_message_handler(Admin_ad_message, content_types=ct.all(), state=Admin_state.ad_message)
dp.register_message_handler(Admin_ad_message_type, content_types=[ct.TEXT], state=Admin_state.ad_users_type)

# Channel

dp.register_message_handler(admin_change_group, content_types=[ct.TEXT], state=Admin_state.change_group)
dp.register_message_handler(admin_changed_group, content_types=[ct.TEXT], state=Admin_state.changed_group)
dp.register_message_handler(admin_add_group_name, content_types=[ct.TEXT], state=Admin_state.add_group_name)
dp.register_message_handler(admin_add_channel_link, content_types=[ct.TEXT], state=Admin_state.add_channel_link)

# Uc price
dp.register_message_handler(admin_uc_prices, content_types=[ct.TEXT], state=Admin_state.uc_prices)
dp.register_message_handler(admin_add_uc_amount, content_types=[ct.TEXT], state=Admin_state.uc_add_amount)
dp.register_message_handler(admin_add_uc_price, content_types=[ct.TEXT], state=Admin_state.uc_add_price)
dp.register_message_handler(Admin_uc_del, content_types=[ct.TEXT], state=Admin_state.uc_del)

"""
USER APPS
"""

dp.register_message_handler(user_main_menu, content_types=[ct.TEXT], state=User_state.main_menu)
dp.register_message_handler(user_get_uc, content_types=[ct.TEXT], state=User_state.get_uc)
dp.register_message_handler(user_sub_menu, content_types=[ct.TEXT], state=User_state.sub_menu)
dp.register_message_handler(user_get_thought, content_types=[ct.TEXT], state=User_state.get_thought)

dp.register_callback_query_handler(user_buy_uc, state=User_state.buy_uc_main)
dp.register_callback_query_handler(user_buy_check, state=User_state.buy_uc_check)

dp.register_message_handler(user_buy_id, content_types=[ct.TEXT], state=User_state.buy_uc_id)
dp.register_message_handler(user_buy_uc_chek, content_types=[ct.DOCUMENT, ct.PHOTO, ct.TEXT], state=User_state.buy_uc_chek)

"""

dp.register_message_handler(user_audiobook_type, content_types=[ct.TEXT], state=User_state.audiobook_type)

dp.register_message_handler(user_free_books, content_types=[ct.TEXT], state=User_state.free_books)

dp.register_message_handler(user_premium_books, content_types=[ct.TEXT], state=User_state.premium_books)


dp.register_message_handler(search_books, content_types=[ct.TEXT], state=User_state.search_books)

dp.register_message_handler(user_audiobooks, content_types=[ct.TEXT], state=User_state.audiobooks)

dp.register_message_handler(user_book_type, content_types=[ct.TEXT])

dp.register_callback_query_handler(on_callback_query, text_startswith=["click_", "payme_", "visa_"])
"""


# CHAT
# from apps.chat import *
# dp.register_message_handler(usermanager)#, content_types=ct.NEW_CHAT_MEMBERS)
