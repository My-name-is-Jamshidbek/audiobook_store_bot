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
        await Admin_state.admin_book_add_name.set()
    elif m.text in get_premium_books():
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await state.update_data(premium_book_name = m.text)
        await Admin_state.book_main_menu.set()


async def admin_book_main_menu(m: m, state: s):
    data = await state.get_data()
    if m.text == "Chiqish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "Kitobni o'chirish":
        await m.answer("Kitobni o'chirishga aminmisiz?", reply_markup=keyboardbutton(["HA kitob o'chirilsin", "YO'Q bekor qilish"]))
        await Admin_state.book_delete.set()
    elif m.text == "Audioversiya":
        r_m = f"{get_premium_book_description(book_name=data.get('premium_book_name'))}\n\n💰Asar narxi - {get_premium_book_price(book_name=data.get('premium_book_name'))} soʻm"
        await m.answer_photo(
            photo=InputFile(get_premium_book_photo(book_name=data.get('premium_book_name'))),
            caption=r_m,
        )
        audios = get_premium_audiobook_address(data.get('premium_book_name'))
        i = 0
        for audio in audios.split("_"):
            i+=1
            await m.answer_audio(
                audio=InputFile(audio),
                caption=f"{i}-qism",
                protect_content=True,
            )
    elif m.text == "Audio va elektron versiya":
        r_m = f"{get_premium_audiobook_description(data.get('premium_book_name'))}\n\n💰Audiokitob narxi - {get_premium_audiobook_price(book_name=data.get('premium_book_name'))} soʻm"
        await m.answer_photo(
            photo=InputFile(get_premium_audiobook_photo(data.get('premium_book_name'))),
            caption=r_m,
        )
        audios = get_premium_audiobook_address(data.get('premium_book_name'))
        
        await m.answer_document(InputFile(get_premium_book_file(book_name=data.get('premium_book_name'))), protect_content=True)
        i = 0
        for audio in audios.split("_"):
            i+=1
            await m.answer_audio(
                audio=InputFile(audio),
                caption=f"{i}-qism",
                protect_content=True,
            )
    elif m.text == "Kitobni tahrirlash" or "Tahrirlash":
        await m.answer("Kitobni tahrirlamoqchi bo'lgan malumotingizni tanlang:",
                       reply_markup=keyboardbutton([
                           "Kitob nomi",
                           "Audiokitob narhi",
                           "Audiokitob rasmi",
                           "Audiokitob audiosi",
                           "Audiokitob malumoti",
                           "Audio narhi",
                           "Audio rasmi",
                           "Elektron fayli",
                           "Audio malumoti",
                           "Chiqish"
                       ]))
        await Admin_state.premium_book_update_main_menu.set()


async def premium_book_update_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Tahrirlash", "Kitobni o'chirish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.text == "Kitob nomi":
        await m.answer("Kitobning yangi nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_name.set()
    elif m.text == "Audiokitob narhi":
        await m.answer("Kitobning yangi Audiokitob narhini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_audiobook_update_price.set()
    elif m.text == "Audiokitob rasmi":
        await m.answer("Kitobning yangi Audiokitob rasmini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_audiobook_update_photo.set()
    elif m.text == "Audiokitob audiosi":
        await m.answer("Kitobning yangi Audiokitob audiosini kiriting:\nHar bitta fayl 1 qism hisoblanadi", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_audiobook_update_audio.set()
    elif m.text == "Audiokitob malumoti":
        await m.answer("Kitobning yangi Audiokitob malumotini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_audiobook_update_about.set()
    elif m.text == "Audio narhi":
        await m.answer("Kitobning yangi Audio narhini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_price.set()
    elif m.text == "Audio rasmi":
        await m.answer("Kitobning yangi Audio rasmini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_photo.set()
    elif m.text == "Elektron fayli":
        await m.answer("Kitobning yangi Elektron faylini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_file.set()
    elif m.text == "Audio malumoti":
        await m.answer("Kitobning yangi Audio malumotini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.premium_book_update_about.set()



async def admin_book_delete(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "HA kitob o'chirilsin":
        delete_premium_book(book_name)
        await m.answer("Kitob muvaffaqiyatli o'chirildi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "YO'Q bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()



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
            await state.update_data(admin_book_add_name=m.text)
            await m.answer("Audioversiya muqovasi uchun fayl shaklida rasm yuboring:")
            await Admin_state.admin_book_add_photo.set()


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
                await state.update_data(admin_book_add_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli saqlandi!")
                await m.answer("Audioversiya sarlavhasi uchun malumotlarni yuboring:")
                await Admin_state.admin_book_add_description.set()
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
        await state.update_data(admin_book_add_description=m.text)
        await m.answer("Audioversiya narhini yuboring:")
        await Admin_state.admin_book_add_price.set()


async def admin_book_add_price(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        if m.text.isdigit():
            await state.update_data(admin_book_add_price=m.text)
            await m.answer("Kitobning elektron faylini yuboring:")
            await Admin_state.admin_book_add_file.set()
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
            data = await state.get_data()
            file_name = f"{data.get('admin_book_add_name')}.{m.document.file_name.split('.')[-1]}"
            save_path = os.path.join("database/files/", file_name)
            try:
                await bot.download_file_by_id(file_id, save_path, timeout=1000)
                await state.update_data(admin_book_add_file=save_path)
                await m.answer("File muvaffaqiyatli saqlandi!\nAudio va elektron versiya sarlavhasi uchun fayl shaklida rasm yuboring:")
                await Admin_state.admin_audiobook_add_photo.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile word yoki pdf formatida bo'lishi zarur!")
    else:
        await m.answer("Word yoki pdf file ni document shaklida jo'nating!")



async def admin_audiobook_add_photo(m: m, state: s):
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
                await state.update_data(admin_audiobook_add_photo=save_path)
                await m.answer("Rasm muvaffaqiyatli saqlandi!")
                await m.answer("Audio va elektron versiya sarlavhasi uchun malumotlarni yuboring:")
                await Admin_state.admin_audiobook_add_description.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")


async def admin_audiobook_add_description(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        await state.update_data(admin_audiobook_add_description=m.text)
        await m.answer("Audio va elektron versiya narhini kiriting:")
        await Admin_state.admin_audiobook_add_price.set()


async def admin_audiobook_add_price(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    else:
        if m.text.isdigit():
            await state.update_data(admin_audiobook_add_price=m.text)
            await m.answer("Audio va elektron versiya audio faylini (mp3) formatida yuboring:\nHar bir fayl bir qism hisoblanadi!")
            await Admin_state.admin_audiobook_add_audio.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")

async def admin_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("admin_audiobook_add_audio")) > 1:
            add_premium_book(
                book_name=data.get("admin_book_add_name"),
                book_photo=data.get("admin_book_add_photo"),
                book_description=data.get("admin_book_add_description"),
                book_price=data.get("admin_book_add_price"),
                book_address=data.get("admin_book_add_file"),

                audiobook_photo=data.get("admin_audiobook_add_photo"),
                audiobook_description=data.get("admin_audiobook_add_description"),
                audiobook_price=data.get("admin_audiobook_add_price"),
                audiobook_address=data.get("admin_audiobook_add_audio"),
            )
            await m.answer("Kitob muvaffaqiyatli qo'shildi!")
            await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                            "Chiqish"]))
            await Admin_state.premium_books.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        data = await state.get_data()
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            data = await state.get_data()
            book_name = data.get("admin_book_add_name")
            old_names = data.get("admin_audiobook_add_audio")
            if old_names:audio_file_path = f"database/audios/{book_name}-{str(len(old_names.split('_'))+1)}.{m.audio.file_name.split('.')[-1]}"
            else:audio_file_path = f"database/audios/{book_name}-1.{m.audio.file_name.split('.')[-1]}"
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(admin_audiobook_add_audio=audio_file_path)
            else:
                await state.update_data(admin_audiobook_add_audio=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("Fayl muvaffaqiyatli saqlandi keyingi qismni kiritishingiz mumkin:", reply_markup=keyboardbutton(["Tugatish", "Bekor qilish", ]))
        except Exception as e:
            print(e)
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")



async def admin_free_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitob qo'shish":
        await m.answer("Kitob nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_add_name.set()
    elif m.text in get_free_books():
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(m.text)),
                        caption=f" "
                        f"{get_free_book_description(m.text)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await state.update_data(free_book_name=m.text)
        await Admin_state.free_book_main_menu.set()


async def admin_free_book_main_menu(m: m, state: s):
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
                           "Kitob sarlavhasi",
                           "Kitob rasmi",
                           "Audiofayllar",
                           "Chiqish",
                       ], row=2))
        await Admin_state.admin_free_book_update_main_menu.set()
    elif m.text == "Audiolarni yuklash":
        data = await state.get_data()
        audios = get_free_book_address(data.get('free_book_name'))
        i = 0
        for audio in audios.split("_"):
            i+=1
            await m.answer_audio(
                audio=InputFile(audio),
                caption=f"{i}-qism",
                protect_content=True,
            )

async def admin_free_book_update_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f" "
                       f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text == "Kitob nomi":
        await m.answer("Kitobning yangi nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_name.set()
    elif m.text == "Kitob sarlavhasi":
        await m.answer("Kitobning beepul yangi sarlavhasini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_description.set()
    elif m.text == "Kitob rasmi":
        await m.answer("Kitobning yangi rasmini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_photo.set()
    elif m.text == "Audiofayllar":
        await m.answer("Kitobning yangi Audiofayllarini yuboring:\nHar bir fayl bir qism hisoblanadi!", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.free_book_update_group.set()


async def free_book_update_photo(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f" "
                       f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
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
                await m.answer_photo(
                                photo=InputFile(get_free_book_photo(book_name)),
                                caption=f" "
                            f"{get_free_book_description(book_name)}\n",
                                reply_markup=keyboardbutton(
                    [
                        "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                        "Chiqish",
                    ]
                ))
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
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f" "
                       f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
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
            book_name=m.text
            await state.update_data(free_book_name=m.text)
            await m.answer("Kitob nomi muvaffaqiyatli o'zgartirildi!")
            await m.answer_photo(
                            photo=InputFile(get_free_book_photo(book_name)),
                            caption=f" "
                        f"{get_free_book_description(book_name)}\n",
                            reply_markup=keyboardbutton(
                [
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
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f" "
                       f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    else:
        await m.answer("Kitobning sarlavhasi o'zgartirildi!")
        update_free_book_description(book_name, m.text)
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f" "
                       f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()


async def free_book_update_group(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("free_book_name")
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(book_name)),
                        caption=f"{get_free_book_description(book_name)}\n",
                        reply_markup=keyboardbutton(
            [
                "Kitobni tahrirlash",
                        "Audiolarni yuklash",
                        "Kitobni o'chirish",
                "Chiqish",
            ]
        ))
        await Admin_state.free_book_main_menu.set()
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("admin_free_book_update_audiobooks")) > 1:
            update_free_book_address(book_name, data.get("admin_free_book_update_audiobooks"))
            await m.answer_photo(
                    photo=InputFile(get_free_book_photo(book_name)),
                    caption=f"{get_free_book_description(book_name)}",
                    reply_markup=keyboardbutton(
                        [
                            "Kitobni tahrirlash",
                            "Audiolarni yuklash",
                            "Kitobni o'chirish",
                            "Chiqish",
                        ]
                    ))
            await Admin_state.free_book_main_menu.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            data = await state.get_data()
            old_names = data.get("admin_free_book_update_audiobooks")
            if old_names:audio_file_path = f"database/audios/{book_name}-{str(len(old_names.split('_'))+1)}.{m.audio.file_name.split('.')[-1]}"
            else:audio_file_path = f"database/audios/{book_name}-1.{m.audio.file_name.split('.')[-1]}"
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(admin_free_book_update_audiobooks=audio_file_path)
            else:
                await state.update_data(admin_free_book_update_audiobooks=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("Fayl muvaffaqiyatli saqlandi keyingi qismni kiritishingiz mumkin:", reply_markup=keyboardbutton(["Tugatish", "Bekor qilish", ]))
        except Exception as e:
            print(e)
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")

    

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
                photo=InputFile(get_free_book_photo(book_name)),
                caption=f"{get_free_book_description(book_name)}\n",
                reply_markup=keyboardbutton(
                    [
                        "Kitobni tahrirlash",
                        "Audiolarni yuklash",
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
                await m.answer("Kitob audio (mp3) fayllarini yuboring:\nHar bitta fayl bir qism hisoblanadi!")
                await Admin_state.free_book_add_group.set()
            except:
                await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
        else:
            await m.answer("File formati noto'g'ri!\nFile jpg yoki png formatida bo'lishi zarur!")
    else:
        await m.answer("jpg yoki png file ni document shaklida jo'nating!")


async def admin_free_book_add_group(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
    elif m.text == "Tugatish":
        data = await state.get_data()
        if len(data.get("admin_free_book_add_group")) > 1:
            data = await state.get_data()
            add_free_book(
                book_name=data.get("free_book_add_name"),
                audiobook_address=data.get("admin_free_book_add_group"),
                book_description=data.get("free_book_add_description"),
                book_photo=data.get("free_book_add_photo")
            )
            await m.answer("Kitob muvaffaqiyatli qo'shildi!")
            await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
                get_free_books() + ["Kitob qo'shish", "Chiqish"]))
            await Admin_state.free_books.set()
        else:
            await m.answer("Siz hali audio fayl kiritmadingiz!")
    elif m.audio:
        mes = await m.answer("Fayl tekshirilmoqda...")
        audio_file_id = m.audio.file_id
        await mes.edit_text("Fayl yuklab olinmoqda...")
        try:
            data = await state.get_data()
            book_name = data.get("free_book_add_name")
            old_names = data.get("admin_free_book_add_group")
            if old_names:audio_file_path = f"database/audios/{book_name}-{str(len(old_names.split('_'))+1)}.{m.audio.file_name.split('.')[-1]}"
            else:audio_file_path = f"database/audios/{book_name}-1.{m.audio.file_name.split('.')[-1]}"
            await bot.download_file_by_id(audio_file_id, audio_file_path, timeout=1000)
            if not old_names:
                await state.update_data(admin_free_book_add_group=audio_file_path)
            else:
                await state.update_data(admin_free_book_add_group=old_names+"_"+audio_file_path)
            await mes.delete()
            await m.answer("Fayl muvaffaqiyatli saqlandi keyingi qismni kiritishingiz mumkin:", reply_markup=keyboardbutton(["Tugatish", "Bekor qilish", ]))
        except Exception as e:
            print(e)
            await mes.delete()
            await m.answer("Ayrim muammolar sababli faylni yuklab olishni iloji bo'lmadi iltimos qayta yuboring!")
    else:
        await m.answer("mp3 file ni document shaklida jo'nating!")

