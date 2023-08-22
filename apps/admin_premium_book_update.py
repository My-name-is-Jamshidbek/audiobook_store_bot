import os
import uuid

from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from database.database import *
from loader import bot
from states import *


async def premium_book_update_name(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        if m.text in get_premium_books():
            await m.answer("Bunday nomli premium kitob mavjud iltimos boshqa nom tanlang!")
        else:
            update_premium_book_name(book_name, new_name=m.text)
            await state.update_data(premium_book_name=m.text)
            await m.answer("Kitob nomi muvaffaqiyatli o'zgartirildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()


async def premium_audiobook_update_price(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        if m.text.isdigit():
            update_premium_audiobook_price(book_name, m.text)
            await m.answer("Kitob narxi muvaffaqiyatli o'zgartirildi!")
            await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
            await Admin_state.book_main_menu.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")


async def premium_audiobook_update_photo(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.document:
        file_id = m.document.file_id

        # Get the MIME type of the file
        mime_type = m.document.mime_type
        if mime_type == 'image/png' or mime_type == 'image/jpeg' or mime_type == 'image/jpg':
            # Save the file
            file_name = str(uuid.uuid4())+"."+m.document.file_name.split(".")[-1]
            save_path = os.path.join("database/media/", file_name)
            try:
                await bot.download_file_by_id(file_id, save_path, timeout=1000)
                update_premium_audiobook_photo_type(book_name=book_name, audiobook_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli o'zgartirildi!")
                await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
                await Admin_state.book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")


async def premium_audiobook_update_about(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        await m.answer("Kitobning sarlavhasi o'zgartirildi!")
        update_premium_audiobook_description(book_name, m.text)
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()


async def premium_book_update_price(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        if m.text.isdigit():
            await m.answer("Kitob narxi muvaffaqiyatli o'zgartirildi!")
            update_premium_book_price(book_name, m.text)
            await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
            await Admin_state.book_main_menu.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")


async def premium_book_update_photo(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.document:
        file_id = m.document.file_id

        # Get the MIME type of the file
        mime_type = m.document.mime_type
        if mime_type == 'image/png' or mime_type == 'image/jpeg' or mime_type == 'image/jpg':
            # Save the file
            file_name = str(uuid.uuid4())+"."+m.document.file_name.split(".")[-1]
            save_path = os.path.join("database/media/", file_name)
            try:
                await bot.download_file_by_id(file_id, save_path, timeout=1000)
                update_premium_book_photo_type(book_name=book_name, book_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli o'zgartirildi!")
                await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
                await Admin_state.book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")


async def premium_book_update_file(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.text:
        update_premium_book_file(book_name, m.text)
        await m.answer("id muvaffaqiyatli saqlandi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()


async def premium_book_update_about(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        await m.answer("Kitobning sarlavhasi o'zgartirildi!")
        update_premium_book_description(book_name, m.text)
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()


async def premium_audiobook_update_audio(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.text:
        data = await state.get_data()
        update_premium_audiobook_audio(book_name, m.text)
        await m.answer("Kitob audiosi muvaffaqiyatli o'zgartirildi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
