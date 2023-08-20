"""
app file
"""
from aiogram.types import ContentType as ct, PreCheckoutQuery

from apps.admin import *
from apps.user import *
from loader import dp

from apps.login import cmd_start, fullname, phone_number, register
from apps.payment_helper import on_callback_query
from apps.admin_premium_book_update import premium_book_update_name, premium_audiobook_update_price, premium_audiobook_update_photo, premium_audiobook_update_about, premium_book_update_price, premium_book_update_photo, premium_book_update_file, premium_book_update_about, premium_audiobook_update_audio
from states import User_state, Admin_state

# cmd start
dp.register_message_handler(cmd_start, commands=['start'])

"""
PAYMENT
"""

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_check_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=[ct.SUCCESSFUL_PAYMENT])
async def succesfull_pay(m: m):
    try:
        if m.successful_payment.invoice_payload.split("_")[1] == "e":
            add_user_premium_book(tg_id=m.from_user.id, book_id=get_premium_book_id(m.successful_payment.invoice_payload.split("_")[0]))
            await m.answer(f"{m.successful_payment.invoice_payload} nomli kitobning elektron versiyasi uchun {m.successful_payment.total_amount // 100} {m.successful_payment.currency} to'lov qilindi kitobni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin.", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        elif m.successful_payment.invoice_payload.split("_")[1] == "a":
            add_user_premium_audiobook(tg_id=m.from_user.id, book_id=get_premium_book_id(m.successful_payment.invoice_payload.split("_")[0]))
            await m.answer(f"{m.successful_payment.invoice_payload} nomli kitobning to'liq uchun {m.successful_payment.total_amount // 100} {m.successful_payment.currency} to'lov qilindi kitobni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin.", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
    except:
        await m.answer(f"Tizimda xatolik yuzaga keldi iltimos admin bilan bog'laning", reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
    await User_state.main_menu.set()


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
dp.register_message_handler(admin_book_add_name, content_types=[ct.TEXT], state=Admin_state.admin_book_add_name)

# Admin book add photo
dp.register_message_handler(admin_book_add_photo, content_types=[ct.TEXT, ct.DOCUMENT], state=Admin_state.admin_book_add_photo)

# Admin book add description
dp.register_message_handler(admin_book_add_description, content_types=[ct.TEXT],
                            state=Admin_state.admin_book_add_description)

# Admin book add price
dp.register_message_handler(admin_book_add_price, content_types=[ct.TEXT], state=Admin_state.admin_book_add_price)

# Admin book add file
dp.register_message_handler(admin_book_add_file, content_types=[ct.TEXT, ct.DOCUMENT],
                            state=Admin_state.admin_book_add_file)

# Admin audiobook add photo
dp.register_message_handler(admin_audiobook_add_photo, content_types=[ct.DOCUMENT, ct.TEXT], state=Admin_state.admin_audiobook_add_photo)

# Admin audiobook add description
dp.register_message_handler(admin_audiobook_add_description, content_types=[ct.TEXT], state=Admin_state.admin_audiobook_add_description)

# Admin audiobook add price
dp.register_message_handler(admin_audiobook_add_price, content_types=[ct.TEXT], state=Admin_state.admin_audiobook_add_price)

# Admin audiobook add audio
dp.register_message_handler(admin_book_add_audio, content_types=[ct.AUDIO, ct.TEXT, ct.DOCUMENT, ct.all()], state=Admin_state.admin_audiobook_add_audio)


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

# Admin free book add group
dp.register_message_handler(admin_free_book_add_group, content_types=[ct.TEXT], state=Admin_state.free_book_add_group)

# Admin free book add photo
dp.register_message_handler(admin_free_book_add_photo, content_types=[ct.DOCUMENT, ct.TEXT], state=Admin_state.free_book_add_photo)

# Admin freee book main menu
dp.register_message_handler(admin_free_book_main_menu, content_types=[ct.TEXT], state=Admin_state.free_book_main_menu)

# Admin free book delete
dp.register_message_handler(admin_free_book_delete, content_types=[ct.TEXT], state=Admin_state.free_book_delete)

# Admin contact us
dp.register_message_handler(admin_contact_us, content_types=[ct.TEXT], state=Admin_state.contact_us)

# Admin contact us change
dp.register_message_handler(admin_contact_us_change, content_types=[ct.TEXT], state=Admin_state.contact_us_change)

# Admin books update


# Admin free books update
dp.register_message_handler(admin_free_book_update_main_menu, content_types=[ct.TEXT], state=Admin_state.admin_free_book_update_main_menu)

dp.register_message_handler(free_book_update_name, content_types=[ct.TEXT], state=Admin_state.free_book_update_name)

dp.register_message_handler(free_book_update_description, content_types=[ct.TEXT], state=Admin_state.free_book_update_description)

dp.register_message_handler(free_book_update_group, content_types=[ct.TEXT], state=Admin_state.free_book_update_group)

dp.register_message_handler(free_book_update_photo, content_types=[ct.TEXT, ct.DOCUMENT], state=Admin_state.free_book_update_photo)

# Admin premium books update
dp.register_message_handler(premium_book_update_main_menu, content_types=[ct.TEXT], state=Admin_state.premium_book_update_main_menu)
dp.register_message_handler(premium_book_update_name, content_types=[ct.TEXT], state=Admin_state.premium_book_update_name)
dp.register_message_handler(premium_audiobook_update_price, content_types=[ct.TEXT], state=Admin_state.premium_audiobook_update_price)
dp.register_message_handler(premium_audiobook_update_photo, content_types=[ct.TEXT, ct.DOCUMENT], state=Admin_state.premium_audiobook_update_photo)
dp.register_message_handler(premium_audiobook_update_about, content_types=[ct.TEXT], state=Admin_state.premium_audiobook_update_about)
dp.register_message_handler(premium_book_update_price, content_types=[ct.TEXT], state=Admin_state.premium_book_update_price)
dp.register_message_handler(premium_book_update_photo, content_types=[ct.TEXT, ct.DOCUMENT], state=Admin_state.premium_book_update_photo)
dp.register_message_handler(premium_book_update_file, content_types=[ct.TEXT, ct.DOCUMENT], state=Admin_state.premium_book_update_file)
dp.register_message_handler(premium_book_update_about, content_types=[ct.TEXT], state=Admin_state.premium_book_update_about)
dp.register_message_handler(premium_audiobook_update_audio, content_types=[ct.TEXT, ct.AUDIO], state=Admin_state.premium_audiobook_update_audio)


"""
USER APPS
"""

# Register

dp.register_message_handler(fullname, content_types=[ct.TEXT], state=User_state.fullname)

dp.register_message_handler(phone_number, content_types=[ct.TEXT, ct.CONTACT], state=User_state.phone_number)

dp.register_message_handler(user_main_menu, content_types=[ct.TEXT], state=User_state.main_menu)

dp.register_message_handler(user_audiobook_type, content_types=[ct.TEXT], state=User_state.audiobook_type)

dp.register_message_handler(user_free_books, content_types=[ct.TEXT], state=User_state.free_books)

dp.register_message_handler(user_premium_books, content_types=[ct.TEXT], state=User_state.premium_books)

dp.register_message_handler(register, content_types=[ct.TEXT], state=User_state.register)

dp.register_message_handler(search_books, content_types=[ct.TEXT], state=User_state.search_books)

dp.register_message_handler(user_audiobooks, content_types=[ct.TEXT], state=User_state.audiobooks)

dp.register_message_handler(user_book_type, content_types=[ct.TEXT])

dp.register_callback_query_handler(on_callback_query, text_startswith=["click_", "payme_"])
