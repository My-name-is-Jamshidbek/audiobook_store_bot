"""
user apps
"""
import os
import uuid

from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from database.database import *
from loader import bot
from states import *


async def admin_main_menu(m: m, state: s):
    if m.text == "Audioteka 🎧":
        await m.answer("Kitob turini tanlang:", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Biz bilan aloqa 📞":
        await m.answer(get_latest_contact_message(), reply_markup=keyboardbutton(["O'zgartirish", "Chiqish"]))
        await Admin_state.contact_us.set()


async def admin_contact_us(m: m, state: s):
    if m.text=="O'zgartirish":
        await m.answer("Yangi habarni yuboring:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.contact_us_change.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞"]))
        await Admin_state.main_menu.set()


async def admin_contact_us_change(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞"]))
        await Admin_state.main_menu.set()
    elif m.text:
        insert_contact_message(m.text)
        await m.answer("Habar yangilandi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞"]))
        await Admin_state.main_menu.set()


async def admin_book_type(m: m, state: s):
    if m.text == "Premium":
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "Beepul":
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_free_books()+["Kitob qo'shish",
                                                                        "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞"]))
        await Admin_state.main_menu.set()

async def admin_premium_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitob qo'shish":
        await m.answer("Kitob nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_add_name.set()
    elif m.text in get_premium_books():
        await m.answer(f"Kitob nomi: {m.text}\n"
                       f"Kitob ma'lumoti: {get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi: {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Audio va elektron format 📔",
                "Kitobni o'chirish",
                "Chiqish"
            ]
        ))
        await state.update_data(premium_book_name = m.text)
        await Admin_state.book_main_menu.set()


async def admin_book_add_name(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        if m.text in get_premium_books():
            await m.answer("Bunday nomli premium kitob mavjud iltimos boshqa nom tanlang!")
        else:
            await state.update_data(premium_book_add_name=m.text)
            await m.answer("Kitob malumotlarini yuboring:")
            await Admin_state.premium_book_add_description.set()

async def admin_book_add_description(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        await state.update_data(premium_book_add_description=m.text)
        await m.answer("Kitob audio (mp3) formatini yuboring:")
        await Admin_state.premium_book_add_audio.set()


async def admin_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        audio_file_path = "database/audios/" + str(uuid.uuid4())+"."+m.audio.file_name.split(".")[-1]
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            await state.update_data(premium_book_add_audio=audio_file_path)
            await mes.delete()
            await m.answer("File muvaffaqiyatli saqlandi!\nKitobning elektron nusxasini (pdf, word) yuborishingiz mumkin:")
            await Admin_state.premium_book_add_file.set()
        except:
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")



async def admin_book_add_price(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        if m.text.isdigit():
            data = await state.get_data()
            add_book(
                book_name=data.get("premium_book_add_name"),
                audiobook_address=data.get("premium_book_add_audio"),
                file_address=data.get("premium_book_add_file"),
                premium_book=1,
                book_description=data.get("premium_book_add_description"),
                book_price=m.text
                     )
            await m.answer("kitob muvaffaqiyatli qo'shildi!")
            await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books() + [
                "Kitob qo'shish",
                                                                                                              "Chiqish"]))
            await Admin_state.premium_books.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")

async def admin_book_add_file(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
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
                await state.update_data(premium_book_add_file=save_path)
                await m.answer("File muvaffaqiyatli saqlandi!\nKitobning narxini yuborishingiz mumkin:")
                await Admin_state.premium_book_add_price.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")


async def admin_book_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Premium auidokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_premium_books() + ["Kitob qo'shish",
                                                                       "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "Kitobni o'chirish":
        await m.answer("Kitobni o'chirishga aminmisiz?", reply_markup=keyboardbutton(["HA kitob o'chirilsin", "YO'Q bekor qilish"]))
        await Admin_state.book_delete.set()
    elif m.text == "Audio format 🎧":
        await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name)))
    elif m.text == "Audio va elektron format 📔":
        await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name)))
        await bot.send_document(m.chat.id, InputFile(get_premium_book_file_address_path(book_name)))


async def admin_book_delete(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "HA kitob o'chirilsin":
        delete_premium_book(book_name)
        await m.answer("Kitob muvaffaqiyatli o'chirildi!")
        await m.answer("Premium auidokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_premium_books() + ["Kitob qo'shish",
                                                                       "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "YO'Q bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer(get_premium_book_description(name=book_name), reply_markup=keyboardbutton([" Audio format 🎧", "Audio va elektron format 📔", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()


async def admin_free_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitob qo'shish":
        await m.answer("Kitob nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_add_name.set()
    elif m.text in get_free_books():
        await m.answer(f"Kitob nomi: {m.text}\n"
                       f"Kitob ma'lumoti: {get_free_book_description(name=m.text)}\n", reply_markup=keyboardbutton([" Audio format 🎧", "Audio va elektron format 📔", "Kitobni o'chirish", "Chiqish"]))
        await state.update_data(free_book_name=m.text)
        await Admin_state.free_book_main_menu.set()


async def admin_free_book_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")

    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitobni o'chirish":
        await m.answer("Kitobni o'chirishga aminmisiz?",
                       reply_markup=keyboardbutton(["HA kitob o'chirilsin", "YO'Q bekor qilish"]))
        await Admin_state.free_book_delete.set()
    elif m.text == "Audio format 🎧":
        # Send the audio file to the user
        await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name)))
    elif m.text == "Audio va elektron format 📔":
        # Send the audio file and document (if available) to the user
        await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name)))
        file_address = get_free_book_file_address(book_name)
        if file_address:
            await bot.send_document(m.chat.id, InputFile(file_address))


async def admin_free_book_delete(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")

    if m.text == "HA kitob o'chirilsin":
        # Delete the free book from the database
        delete_free_book(book_name)
        await m.answer("Kitob muvaffaqiyatli o'chirildi!")
        await m.answer("Beepul auidokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.text == "YO'Q bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer(get_free_book_description(name=book_name), reply_markup=keyboardbutton(
            [" Audio format 🎧", "Audio va elektron format 📔", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.free_book_main_menu.set()


async def admin_free_book_add_name(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_free_books() +
                                                                                     ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    else:
        if m.text in get_free_books():
            await m.answer("Bunday nomli beepul kitob mavjud iltimos boshqa nom tanlang!")
        else:
            await state.update_data(free_book_add_name=m.text)
            await m.answer("Kitob malumotlarini yuboring:")
            await Admin_state.free_book_add_description.set()


async def admin_free_book_add_description(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    else:
        await state.update_data(free_book_add_description=m.text)
        await m.answer("Kitob audio (mp3) formatini yuboring:")
        await Admin_state.free_book_add_audio.set()


async def admin_free_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        audio_file_path = "database/audios/" + str(uuid.uuid4()) + "." + m.audio.file_name.split(".")[-1]
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            await state.update_data(free_book_add_audio=audio_file_path)
            await mes.delete()
            await m.answer("File muvaffaqiyatli saqlandi!\nKitobning elektron nusxasini (pdf, word) yuborishingiz mumkin:")
            await Admin_state.free_book_add_file.set()
        except:
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")


async def admin_free_book_add_file(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.document:
        file_id = m.document.file_id

        # Get the MIME type of the file
        mime_type = m.document.mime_type
        if mime_type == 'application/msword' or mime_type == 'application/pdf':
            # Save the file
            file_name = str(uuid.uuid4()) + "." + m.document.file_name.split(".")[-1]
            save_path = os.path.join("database/files/", file_name)
            try:
                await bot.download_file_by_id(file_id, save_path, timeout=1000)
                # print(save_path)
                data = await state.get_data()
                # print(data)
                add_book(
                    book_name=data.get("free_book_add_name"),
                    audiobook_address=data.get("free_book_add_audio"),
                    file_address=save_path,
                    premium_book=0,
                    book_description=data.get("free_book_add_description"),
                    book_price="0"
                )
                await m.answer("Kitob muvaffaqiyatli qo'shildi!")
                await m.answer("Beepul auidokitoblar ro'yxati:",
                               reply_markup=keyboardbutton(get_free_books() + ["Kitob qo'shish", "Chiqish"]))
                await Admin_state.free_books.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")
