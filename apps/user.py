"""
user app
"""
from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from database.database import *
from loader import bot
from states import *

async def user_main_menu(m: m, state: s):
    if m.text == "Audioteka 🎧":
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text == "Audiokitoblarim 💽":
        await m.answer(get_latest_contact_message())
    elif m.text == "Biz bilan aloqa 📞":
        await m.answer(get_latest_contact_message())
    elif m.text == "Qidirish🔍":
        await m.answer("Qidirish uchun kalit so'zni kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await User_state.search_books.set()


async def search_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(
                           ["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
        await User_state.main_menu.set()
    else:
        keyword = m.text
        result = search_book(keyword)
        if result:
            await m.answer("Natijalar:")
            f, n = f"", 0
            for book in result:
                f += f"{n}. \nKitob nomi: {book[1]} \nKitob malumoti: {book[5]}\n"
                if str(book[4]) == "1":
                    f+=f"Kitob turi: Premium\nKitob narhi: {book[6]}"
                else:
                    f+=f"Kitob turi: Beepul"
            await m.answer(f)
        else:
            await m.answer("Kitob topilmadi.")
        await m.answer("Qidirish uchun kalit so'z yuborishingiz mumkin:")


async def user_audiobook_type(m: m, state: s):
    if m.text == "Premium audiokitoblar 💰":
        await m.answer("Premium audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Chiqish"]))
        await User_state.premium_books.set()
    elif m.text == "Bepul audiokitoblar 🎁":
        await m.answer("Beepul audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_free_books()+["Chiqish"]))
        await User_state.free_books.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
        await User_state.main_menu.set()


async def user_premium_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text in get_premium_books():
        await m.answer(f"Kitob nomi: {m.text}\n"
                       f"Kitob ma'lumoti: {get_premium_book_description(m.text)}\n"
                       f"Narxi: {get_premium_book_price(m.text)}", reply_markup=keyboardbutton([" Audio format 🎧", " Audio va elektron format 📔", "Chiqish"]))
        await state.update_data(premium_book_name=m.text)
        await User_state.premium_book_main_menu.set()


async def user_premium_book_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("Premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Premium audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Chiqish"]))
        await User_state.premium_books.set()
    elif m.text == "Audio format 🎧":
        await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name)))
    elif m.text == "Audio va elektron format 📔":
        await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name)))
        await bot.send_document(m.chat.id, InputFile(get_premium_book_file_address_path(book_name)))


async def user_free_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text in get_free_books():
        await m.answer(f"Kitob nomi: {m.text}\n"
                       f"Kitob ma'lumoti: {get_free_book_description(m.text)}\n",
                       reply_markup=keyboardbutton([" Audio format 🎧", " Audio va elektron format 📔", "Chiqish"]))
        await state.update_data(free_book_name=m.text)
        await User_state.free_book_main_menu.set()


async def user_free_book_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Beepul audiokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_free_books() + ["Chiqish"]))
        await User_state.free_books.set()
    elif m.text == "Audio format 🎧":
        await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name)))
    elif m.text == "Audio va elektron format 📔":
        await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name)))
        await bot.send_document(m.chat.id, InputFile(get_free_book_file_address(book_name)))
