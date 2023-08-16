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
        await m.answer_photo(
                        photo=InputFile(get_book_photo(m.text)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
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
            await m.answer("Kitob muqovasi uchun fayl shaklida rasm yuboring:")
            await Admin_state.premium_book_add_photo.set()

async def admin_book_add_photo(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
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
                await state.update_data(premium_book_add_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli saqlandi!")
                await m.answer("Kitobning sarlavhasi uchun malumotlarni yuboring:")
                await Admin_state.premium_book_add_description.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")
    
async def admin_book_add_description(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        await state.update_data(premium_book_add_description=m.text)
        await m.answer("Kitob audio faylini (mp3) formatida yuboring:\nHar bir fayl bir qism hisoblanadi!")
        await Admin_state.premium_book_add_audio.set()

async def admin_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("premium_book_add_audio")) > 1:
            await m.answer("Kitobning elektron nusxasini (pdf, word) yuborishingiz mumkin:", reply_markup=keyboardbutton(["Bekor qilish"]))
            await Admin_state.premium_book_add_file.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        audio_file_path = "database/audios/" + str(uuid.uuid4())+"."+m.audio.file_name.split(".")[-1]
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            data = await state.get_data()
            old_names = data.get("premium_book_add_audio")
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(premium_book_add_audio=audio_file_path)
            else:
                await state.update_data(premium_book_add_audio=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("Fayl muvaffaqiyatli saqlandi keyingi qismni kiritishingiz mumkin:", reply_markup=keyboardbutton(["Tugatish", "Bekor qilish", ]))
        except Exception as e:
            print(e)
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
                book_photo=data.get("premium_book_add_photo"),
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
    elif m.text == "Kitobni tahrirlash":
        await m.answer("O'zgartirish uchun malumotni tanlang:",
                       reply_markup=keyboardbutton([
                           "Kitob nomi",
                           "Auidiobook",
                           "Elektron format",
                           "Kitob turi",
                           "Kitob sarlavhasi",
                           "Kitob narxi",
                           "Kitob rasmi",
                           "Chiqish",
                       ], row=2))
        await Admin_state.admin_book_update_main_menu.set()
    elif m.text == "Audio format 🎧":
        if len(get_premium_audiobook_path(book_name).split("_"))==1:
            await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name)))
        else:    
            await m.answer("Qismni tanlang:", reply_markup=keyboardbutton([f"{i}-qism" for i in range(1, len(get_premium_audiobook_path(book_name).split("_"))+1)]+["Chiqish"]))
            await Admin_state.premium_book_audio.set()
    elif m.text == "Elektron format 📔":
        await bot.send_document(m.chat.id, InputFile(get_premium_book_file_address_path(book_name)))



async def admin_premium_book_audio(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_premium_book_description(name=book_name)}\n"
                       f"Kitob narhi {get_premium_book_price(name=book_name)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await state.update_data(premium_book_name = book_name)
        await Admin_state.book_main_menu.set()
    elif m.text in [f"{i}-qism" for i in range(1, len(get_premium_audiobook_path(book_name).split("_"))+1)]:
        await bot.send_audio(m.chat.id, InputFile(get_premium_audiobook_path(book_name).split("_")[int(m.text.split("-")[0])-1]))          

async def admin_book_update_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_premium_book_description(name=book_name)}\n"
                       f"Kitob narhi {get_premium_book_price(name=book_name)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.book_main_menu.set()
    elif m.text == "Kitob nomi":
        await m.answer("Kitobning yangi nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_name.set()
    elif m.text == "Auidiobook":
        await m.answer("Hozircha mavjud emas")
    elif m.text == "Elektron format":
        await m.answer("Kitobning yangi elektron faylini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_file.set()
    elif m.text == "Kitob turi":
        await m.answer("Kitobning yangi turini tanlang:", reply_markup=keyboardbutton(["Premium", "Beepul", "Bekor qilish"]))
        await Admin_state.premium_book_update_type.set()
    elif m.text == "Kitob sarlavhasi":
        await m.answer("Kitobning yangi sarlavhasini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_description.set()
    elif m.text == "Kitob rasmi":
        await m.answer("Kitobning yangi rasmini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_photo.set()
    elif m.text == "Kitob narxi":
        await m.answer("Kitobning yangi narxini kirtitng:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_price.set()


async def premium_book_update_file(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
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
                await m.answer(get_premium_book_description(name=book_name), reply_markup=keyboardbutton([" Audio format 🎧", "Elektron format 📔", "Kitobni o'chirish",
                        "Kitobni tahrirlash", "Chiqish"]))
                await Admin_state.book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")


async def premium_book_update_photo(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
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
                await m.answer(get_premium_book_description(name=book_name), reply_markup=keyboardbutton([" Audio format 🎧", "Elektron format 📔", "Kitobni tahrirlash",
                        "Kitobni o'chirish", "Chiqish"]))
                await Admin_state.book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")



async def premium_book_update_price(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.book_main_menu.set()
    else:
        if m.text.isdigit():
            await m.answer("Kitob narxi muvaffaqiyatli o'zgartirildi!")
            update_premium_book_price(book_name, m.text)
            await m.answer(get_premium_book_description(name=book_name), reply_markup=keyboardbutton([" Audio format 🎧", "Elektron format 📔", "Kitobni o'chirish",
                    "Kitobni tahrirlash", "Chiqish"]))
            await Admin_state.book_main_menu.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")

async def premium_book_update_name(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.book_main_menu.set()
    else:
        if m.text in get_premium_books():
            await m.answer("Bunday nomli premium kitob mavjud iltimos boshqa nom tanlang!")
        else:
            update_premium_book_name(book_name, new_name=m.text)
            await state.update_data(premium_book_name=m.text)
            await m.answer("Kitob nomi muvaffaqiyatli o'zgartirildi!")
            await m.answer(get_premium_book_description(name=m.text), reply_markup=keyboardbutton([" Audio format 🎧", "Elektron format 📔", "Kitobni o'chirish",
                    "Kitobni tahrirlash", "Chiqish"]))
            await Admin_state.book_main_menu.set()


async def premium_book_update_description(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.book_main_menu.set()
    else:
        await m.answer("Kitobning sarlavhasi o'zgartirildi!")
        update_premium_book_description(book_name, m.text)
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await state.update_data(premium_book_name = m.text)
        await Admin_state.book_main_menu.set()


async def premium_book_update_type(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=1)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.book_main_menu.set()
    elif m.text in ["Premium", "Beepul"]:
        await m.answer("Kitobning turi o'zgartirildi!")
        update_premium_book_type(book_name)
        await m.answer("Premium auidokitoblar ro'yxati:",
                       reply_markup=keyboardbutton(get_premium_books() + ["Kitob qo'shish",
                                                                       "Chiqish"]))
        await Admin_state.premium_books.set()
   

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
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_premium_book_description(name=m.text)}\n"
                       f"Kitob narhi {get_premium_book_price(name=m.text)} so'm", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await state.update_data(premium_book_name = m.text)
        await Admin_state.book_main_menu.set()


async def admin_free_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitob qo'shish":
        await m.answer("Kitob nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_add_name.set()
    elif m.text in get_free_books():
        await m.answer_photo(
                        photo=InputFile(get_book_photo(m.text, premium=0)),
                        caption=f"<strong>{m.text}</strong>\n"
                        f"{get_free_book_description(name=m.text)}\n",
                        reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
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
    elif m.text == "Kitobni tahrirlash":
        await m.answer("O'zgartirish uchun malumotni tanlang:",
                       reply_markup=keyboardbutton([
                           "Kitob nomi",
                           "Auidiobook",
                           "Elektron format",
                           "Kitob turi",
                           "Kitob sarlavhasi",
                           "Kitob rasmi",
                           "Chiqish",
                       ], row=2))
        await Admin_state.admin_free_book_update_main_menu.set()
    elif m.text == "Audio format 🎧":
        if len(get_free_audiobook_path(book_name).split("_"))==1:
            await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name)))
        else:    
            await m.answer("Qismni tanlang:", reply_markup=keyboardbutton([f"{i}-qism" for i in range(1, len(get_free_audiobook_path(book_name).split("_"))+1)]+["Chiqish"]))
            await Admin_state.free_book_audio.set()
    elif m.text == "Elektron format 📔":
        # Send the audio file and document (if available) to the user
        file_address = get_free_book_file_address(book_name)
        if file_address:
            await bot.send_document(m.chat.id, InputFile(file_address))


async def admin_free_book_update_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text == "Kitob nomi":
        await m.answer("Kitobning yangi nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_name.set()
    elif m.text == "Auidiobook":
        await m.answer("Hozircha mavjud emas")
    elif m.text == "Elektron format":
        await m.answer("Kitobning yangi elektron faylini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_file.set()
    elif m.text == "Kitob turi":
        await m.answer("Kitobning yangi turini tanlang:", reply_markup=keyboardbutton(["Premium", "Beepul", "Bekor qilish"]))
        await Admin_state.free_book_update_type.set()
    elif m.text == "Kitob sarlavhasi":
        await m.answer("Kitobning beepul yangi sarlavhasini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_description.set()
    elif m.text == "Kitob rasmi":
        await m.answer("Kitobning yangi rasmini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_photo.set()


async def free_book_update_file(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_free_book_description(name=m.text)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
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
                update_free_book_file(book_name, save_path)
                await m.answer("File muvaffaqiyatli saqlandi!")
                await m.answer_photo(
                                photo=InputFile(get_book_photo(book_name, premium=0)),
                                caption=f"<strong>{book_name}</strong>\n"
                            f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
                    [
                        " Audio format 🎧",
                        "Elektron format 📔",
                        "Kitobni tahrirlash",
                        "Kitobni o'chirish",
                        "Chiqish",
                    ]
                ))
                await Admin_state.free_book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")


async def free_book_update_photo(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
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
                update_free_book_photo_type(book_name=book_name, book_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli o'zgartirildi!")
                await m.answer(get_free_book_description(name=book_name), reply_markup=keyboardbutton([" Audio format 🎧", "Elektron format 📔", "Kitobni tahrirlash",
                        "Kitobni o'chirish", "Chiqish"]))
                await Admin_state.free_book_main_menu.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")


async def free_book_update_name(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    else:
        if m.text in get_free_books():
            await m.answer("Bunday nomli free kitob mavjud iltimos boshqa nom tanlang!")
        else:
            update_free_book_name(book_name, new_name=m.text)
            await state.update_data(free_book_name=m.text)
            await m.answer("Kitob nomi muvaffaqiyatli o'zgartirildi!")
            await m.answer_photo(
                            photo=InputFile(get_book_photo(m.text, premium=0)),
                            caption=f"<strong>{m.text}</strong>\n"
                        f"{get_free_book_description(name=m.text)}\n", reply_markup=keyboardbutton(
                [
                    " Audio format 🎧",
                    "Elektron format 📔",
                    "Kitobni tahrirlash",
                    "Kitobni o'chirish",
                    "Chiqish",
                ]
            ))
            await Admin_state.free_book_main_menu.set()


async def free_book_update_description(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        print(1)
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    else:
        print(1)
        await m.answer("Kitobning sarlavhasi o'zgartirildi!")
        update_free_book_description(book_name, m.text)
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{m.text}</strong>\n"
                       f"{get_free_book_description(name=m.text)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()


async def free_book_update_type(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text in ["Premium", "Beepul"]:
        if m.text == "Beepul":
            await m.answer("Kitobning narxini kiriting:")
            await Admin_state.update_free_book_type.set()
        else:
            await m.answer("Kitobning turi o'zgartirildi!")
            await m.answer("Beepul auidokitoblar ro'yxati:",
                        reply_markup=keyboardbutton(get_free_books() + ["Kitob qo'shish",
                                                                        "Chiqish"]))
            await Admin_state.free_books.set()


async def update_free_book_type_(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                       f"{get_free_book_description(name=book_name)}\n", reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text.isdigit():
        update_free_book_type(book_name, m.text)
        await m.answer("Kitobning turi o'zgartirildi!")
        await m.answer("Beepul auidokitoblar ro'yxati:",
                    reply_markup=keyboardbutton(get_free_books() + ["Kitob qo'shish",
                                                                    "Chiqish"]))
        await Admin_state.free_books.set()
    
async def admin_free_book_audio(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Chiqish":
        await m.answer_photo(
                        photo=InputFile(get_book_photo(book_name, premium=0)),
                        caption=f"<strong>{book_name}</strong>\n"
                        f"{get_free_book_description(name=book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                " Audio format 🎧",
                "Elektron format 📔",
                "Kitobni tahrirlash",
                "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text in [f"{i}-qism" for i in range(1, len(get_free_audiobook_path(book_name).split("_"))+1)]:
        await bot.send_audio(m.chat.id, InputFile(get_free_audiobook_path(book_name).split("_")[int(m.text.split("-")[0])-1]))          



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
        await m.answer_photo(
                photo=InputFile(get_book_photo(book_name, premium=0)),
                caption=f"<strong>{book_name}</strong>\n"
                f"{get_free_book_description(name=book_name)}\n",
                reply_markup=keyboardbutton(
                    [
                        " Audio format 🎧",
                        "Elektron format 📔",
                        "Kitobni tahrirlash",
                        "Kitobni o'chirish",
                        "Chiqish",
                    ]
                ))
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
        await m.answer("Kitob muqovasi uchun rasm yuboring:")
        await Admin_state.free_book_add_photo.set()

async def admin_free_book_add_photo(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
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
                await state.update_data(free_book_add_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli saqlandi!")
                await m.answer("Kitob audio (mp3) formatini yuboring:\nHar bir yuborilgan fayl bir qism hisoblanadi!")
                await Admin_state.free_book_add_audio.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")
  
async def admin_free_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("free_book_add_audio")) > 1:
            await m.answer("Kitobning elektron nusxasini (pdf, word) yuborishingiz mumkin:")
            await Admin_state.free_book_add_file.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        audio_file_path = "database/audios/" + str(uuid.uuid4()) + "." + m.audio.file_name.split(".")[-1]
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            data = await state.get_data()
            old_names = data.get("free_book_add_audio")
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(free_book_add_audio=audio_file_path)
            else:
                await state.update_data(free_book_add_audio=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("File muvaffaqiyatli saqlandi!\nKeyingi qismni yuborishingiz mumkin:", reply_markup=keyboardbutton(["Bekor qilish", "Tugatish"]))
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
                    book_price="0",
                    book_photo=data.get("free_book_add_photo")
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
