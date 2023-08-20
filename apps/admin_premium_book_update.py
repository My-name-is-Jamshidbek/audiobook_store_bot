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
    elif m.document:
        file_id = m.document.file_id

        # Get the MIME type of the file
        mime_type = m.document.mime_type
        if mime_type == 'application/msword' or mime_type == 'application/pdf':
            # Save the file
            file_name = str(uuid.uuid4())+"."+m.document.file_name.split(".")[-1]
            save_path = os.path.join("database/files/", file_name)
            try:
                await bot.download_file_by_id(file_id, save_path, timeout=1000)
                update_premium_book_file(book_name, save_path)
                await m.answer("File muvaffaqiyatli saqlandi!")
                await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
                await Admin_state.book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")


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
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("premium_audiobook_update_audio")) > 1:
            update_premium_audiobook_audio(book_name, data.get("premium_audiobook_update_audio"))
            await m.answer("Kitob audiosi muvaffaqiyatli o'zgartirildi!")
            await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                            "Chiqish"]))
            await Admin_state.premium_books.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        audio_file_path = "database/audios/" + str(uuid.uuid4())+"."+m.audio.file_name.split(".")[-1]
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            data = await state.get_data()
            old_names = data.get("premium_audiobook_update_audio")
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(premium_audiobook_update_audio=audio_file_path)
            else:
                await state.update_data(premium_audiobook_update_audio=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("Fayl muvaffaqiyatli saqlandi keyingi qismni kiritishingiz mumkin:", reply_markup=keyboardbutton(["Tugatish", "Bekor qilish", ]))
        except Exception as e:
            print(e)
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")

