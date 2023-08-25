"""
log in
"""
from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from aiogram.types import ReplyKeyboardRemove
from buttons.keyboardbuttons import keyboardbutton, share_contact_button
from config import ADMIN_IDS
from database.database import add_user, get_user, user_exists, create_database, add_starter_user, delete_all_user_premium_books
from states import *


async def cmd_start(m: m):
    """
    :param m:
    :return:
    """
#    delete_all_user_premium_books()
 #   create_database()
    if m.from_user.id in ADMIN_IDS:
        await m.answer(
            "Assalomu aleykum admin\nBotga hush kelibsiz\nKerakli menyuni tanlashiniz mumkin.",
            reply_markup=keyboardbutton(["Audioteka 🎧", "Biz bilan aloqa 📞", "Statistika 📊", "Reklama"])
        )
        await Admin_state.main_menu.set()
    else:
        if user_exists(m.from_user.id):
            data = get_user(m.from_user.id)
            await m.answer(f"Assalomu aleykum {data[2]}! Hush kelibsiz, muhtaram vatandosh!  \n\nSiz bu bot yordamida Omar Xalil ijrosidagi hali oʻzbek tiliga tarjima qilinmagan eng sara va noyob kitoblarning audio va elektron formatlarini harid qilib eshitishingiz mumkin.  \n\nBiz bilan birga boʻlganingiz uchun minnatdormiz! Sizni hali koʻplab foydali manbalar bilan siylay olishimizga ishonamiz.")
            await m.answer_video_note(InputFile('video.mp4'))
            await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                           reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
            await User_state.main_menu.set()
        else:
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            await m.answer_video_note(InputFile('video.mp4'))
            await m.answer("Assalomu alaykum! Hush kelibsiz, muhtaram vatandosh! \n\nSiz bu bot yordamida Omar Xalil "
                           "ijrosidagi hali oʻzbek tiliga tarjima qilinmagan eng sara va noyob kitoblarning audio "
                           "va elektron formatlarini harid qilib eshitishingiz mumkin. \n\nBiz bilan birga boʻlganingiz"
                           " uchun minnatdormiz! Sizni hali koʻplab foydali manbalar bilan siylay olishimizga ishonamiz"
                           ".", reply_markup=keyboardbutton(["Ro'yxatdan o'tish"]))
            await User_state.register.set()


async def register(m: m, state: s):
    if m.text == "Ro'yxatdan o'tish":
        await m.answer("Ro'yxatdan o'tish uchun iltimos ism familiyangizni yozib yuboring:", reply_markup=
        ReplyKeyboardRemove())
        await User_state.fullname.set()
    else:
        await m.answer("Botdan foydalanish uchun iltimos ro'yxatdan o'ting!", reply_markup=keyboardbutton(["Ro'yxatdan o'tish"]))


async def fullname(m: m, state: s):
    fullname = m.text
    await state.update_data(fullname=fullname)
    await m.answer("Telefon raqaqamingizni yuboring:", reply_markup=share_contact_button)
    await User_state.phone_number.set()


async def phone_number(m: m, state: s):
    if m.text:
        phone_number = m.text
    elif m.contact:
        phone_number = m.contact.phone_number
    else:
        phone_number = False
        await m.answer("Iltimos telefon raqamingizni yuboring:", reply_markup=share_contact_button)
    if phone_number:
        data = await state.get_data()
        fullname = data.get("fullname")
        add_user(tg_id=m.from_user.id, fullname=fullname, phone_number=phone_number)
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        await User_state.main_menu.set()

