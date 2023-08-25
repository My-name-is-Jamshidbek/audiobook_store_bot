"""
admin apps
"""
import os
import uuid

from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from buttons.inlinekeyboardbuttons import get_group_link_button
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
    elif m.text == "Statistika 📊":
        await m.answer(f"Foydalanuvchilar statistikasi:\nJami: {count_starters_users()} nafar\nRo'yxatdan o'tgan: {all_users_count()} nafar\n\nKitoblar statistikasi:\nJami sotilgan kitoblar: {all_users_premium_books_count()+all_users_premium_audiobooks_count()} ta\nAudio va elektron versiya: {all_users_premium_audiobooks_count()}\nAudio versiya: {all_users_premium_books_count()}")
    elif m.text == "Reklama":
        await m.answer("Reklama habarini yuboring:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.ad_message.set()


async def Admin_ad_message(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()
    else:
        m_id = m.message_id
        await m.answer("Reklama taqdim etilishi kerak bo'lgan foydalanuvchilarni tanlang:", reply_markup=keyboardbutton(["Barcha foydalanuvchilarga", "Ro'yxatdan o'tganlarga", "Kitob sotib olganlarga", "Chiqish"]))
        await state.update_data(ad_m_id=m_id)
        await Admin_state.ad_users_type.set()


async def send_ad(A_ID, m_id, users):
    c, e = 0,0
    _id = await bot.send_message(A_ID, f"Reklama jo'natilmoqda jami {len(users)} nafar")
    for i in users:
        try:
            await bot.forward_message(i, A_ID, m_id,)
            c+=1
        except:
            e+=1
    await _id.delete()
    await bot.send_message(A_ID, f"Reklama jo'natildi\nMuvaffaqiyatli {c}\nMuvaffaqiyatsiz: {e}", reply_to_message_id=m_id)

async def Admin_ad_message_type(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()
    else:
        data = await state.get_data()
        m_id = data.get("ad_m_id")
        A_ID = m.from_user.id
        if m.text == "Barcha foydalanuvchilarga":
            users = get_all_starters_tg_id() 
        elif m.text == "Ro'yxatdan o'tganlarga":
            users = get_all_users_tg_id()
        elif m.text == "Kitob sotib olganlarga":
            users = all_premium_books_users_tg_id()
        users = list(set(list(map(int, users))))
        await send_ad(A_ID=A_ID, m_id=m_id, users=users)
        await m.answer("Asosiy menyu", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()


async def admin_contact_us(m: m, state: s):
    if m.text=="O'zgartirish":
        await m.answer("Yangi habarni yuboring:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.contact_us_change.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()


async def admin_contact_us_change(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()
    elif m.text:
        insert_contact_message(m.text)
        await m.answer("Habar yangilandi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
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
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"]))
        await Admin_state.main_menu.set()

async def admin_premium_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!", reply_markup=keyboardbutton(["Premium", "Beepul", "Chiqish"]))
        await Admin_state.book_type.set()
    elif m.text == "Kitob qo'shish":
        await m.answer("Kitob nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.admin_book_add_name.set()
    elif m.text in get_premium_books():
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Kitobni berish", "Chiqish"]))
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
        audios = get_premium_book_address(data.get('premium_book_name'))
        await m.answer_photo(
            photo=InputFile(get_premium_book_photo(book_name=data.get('premium_book_name'))),
            caption=r_m,
            reply_markup=get_group_link_button(audios)
        )
    elif m.text == "Audio va elektron versiya":
        r_m = f"{get_premium_audiobook_description(data.get('premium_book_name'))}\n\n💰Audiokitob narxi - {get_premium_audiobook_price(book_name=data.get('premium_book_name'))} soʻm"
        audios = get_premium_audiobook_address(data.get('premium_book_name'))
        await m.answer_photo(
            photo=InputFile(get_premium_audiobook_photo(data.get('premium_book_name'))),
            caption=r_m,
            reply_markup=get_group_link_button(audios)
        )
        
    elif m.text == "Kitobni tahrirlash" or m.text == "Tahrirlash":
        await m.answer("Kitobni tahrirlamoqchi bo'lgan malumotingizni tanlang:",
                       reply_markup=keyboardbutton([
                           "Kitob nomi",
                           "Audiokitob narhi",
                           "Audiokitob rasmi",
                           "Audio va elektron guruh",
                           "Audiokitob malumoti",
                           "Audio narhi",
                           "Audio rasmi",
                           "Audio guruh",
                           "Audio malumoti",
                           "Chiqish"
                       ]))
        await Admin_state.premium_book_update_main_menu.set()
    elif m.text == "Kitobni berish":
        await m.answer("Kitob turini tanlang:", reply_markup=keyboardbutton(["Audio versiya", "Audio va elektron versiya", "Chiqish"]))
        await Admin_state.give_book_type.set()


async def admin_give_book_type(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Kitobni berish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif m.text == "Audio versiya" or m.text == "Audio va elektron versiya":
        await state.update_data(give_book_type=m.text)        
        await m.answer("Foydalanuvchi id sini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await Admin_state.give_book_user.set()


async def admin_give_book_user(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Kitobni berish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    elif user_exists(m.text):
        if data.get("give_book_type") == "Audio versiya":
            add_user_premium_book(tg_id=m.text, book_id=get_premium_book_id(book_name=book_name))
        else:
            add_user_premium_audiobook(tg_id=m.text, book_id=get_premium_book_id(book_name=book_name))
        await bot.send_message(m.text, f"Sizga admin tomonidan {book_name} nomli kitob taqdim etildi. Kitobni \"Audiokitoblarim 💽\" bo'limida qabul qilishingiz mumkin!")
        await m.answer("Kitob muvaffaqiyatli berildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Kitobni berish", "Chiqish"]))
        await Admin_state.book_main_menu.set()
    else:
        await m.answer("Foydalanuvchi topilmadi iltimos tekshirib qayta kiriting:")
        
async def premium_book_update_main_menu(m: m, state: s):
    data = await state.get_data()
    book_name = data.get("premium_book_name")
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlang:", reply_markup=keyboardbutton(["Audioversiya", "Audio va elektron versiya", "Kitobni tahrirlash", "Kitobni o'chirish", "Kitobni berish", "Chiqish"]))
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
    elif m.text == "Audio va elektron guruh":
        await m.answer("Kitobning yangi Audiokitob audiosi joylashgan guruh linkini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
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
    elif m.text == "Audio guruh":
        await m.answer("Kitobning yangi Elektron fayli joylashgan guruh linkini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
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
            await m.answer("Audioversiya uchun guruh havolasi:")
            await Admin_state.admin_book_add_file.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")


async def admin_book_add_file(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text:
        await state.update_data(admin_book_add_file=m.text)
        await m.answer("Audio va elektron versiya sarlavhasi uchun fayl shaklida rasm yuboring:")
        await Admin_state.admin_audiobook_add_photo.set()



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
            await m.answer("Audio va elektron versiya uchun guruh linkini kiriting:")
            await Admin_state.admin_audiobook_add_audio.set()
        else:
            await m.answer("Kitob narhini raqam ko'rinishida kiriting!")

async def admin_book_add_audio(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer("Bekor qilindi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()
    elif m.text:
        data = await state.get_data()
        add_premium_book(
            book_name=data.get("admin_book_add_name"),
            book_photo=data.get("admin_book_add_photo"),
            book_description=data.get("admin_book_add_description"),
            book_price=data.get("admin_book_add_price"),
            book_address=data.get("admin_book_add_file"),

            audiobook_photo=data.get("admin_audiobook_add_photo"),
            audiobook_description=data.get("admin_audiobook_add_description"),
            audiobook_price=data.get("admin_audiobook_add_price"),
            audiobook_address=m.text,
        )
        await m.answer("Kitob muvaffaqiyatli qo'shildi!")
        await m.answer("Premium auidokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Kitob qo'shish",
                                                                                                        "Chiqish"]))
        await Admin_state.premium_books.set()


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
        await m.answer("Guruhga havola", reply_markup=get_group_link_button(audios))


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
        await m.answer("Kitobning yangi Audiofayllari joylashgan guruh havolasini yuboring:", reply_markup=keyboardbutton(["Bekor qilish"]))
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
    if m.text:
        update_free_book_address(book_name, m.text)
        await m.answer("Guruh linki muvaffaqiyatli o'zgartirildi!")        
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
                await m.answer("Kitob audio (mp3) fayllari joylashgan guruh havolasini yuboring:")
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
    elif m.text:
        data = await state.get_data()
        add_free_book(
            book_name=data.get("free_book_add_name"),
            audiobook_address=m.text,
            book_description=data.get("free_book_add_description"),
            book_photo=data.get("free_book_add_photo")
        )
        await m.answer("Kitob muvaffaqiyatli qo'shildi!")
        await m.answer("Beepul auidokitoblar ro'yxati:", reply_markup=keyboardbutton(
            get_free_books() + ["Kitob qo'shish", "Chiqish"]))
        await Admin_state.free_books.set()
