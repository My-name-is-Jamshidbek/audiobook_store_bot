"""
user app
"""
from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from buttons.inlinekeyboardbuttons import create_inline_keyboard as inlinekeyboardbutton, get_group_link_button
from database.database import *
from loader import bot
from states import *
# from .payment_helper import get_price_label
from config import ADMIN_IDS, BOT_LINK, ADMIN_ID


async def user_main_menu(m: m, state: s):
    if m.text == "Taklif qilish📣":
        mess = await m.answer(f"<a href=\"{BOT_LINK}?start=taklif_id={m.from_user.id}\">Ushbu botga start bosib ro'yxatdan o'tish orqali PUBG ilovangiz uchun uc yutib oling!</a>")
        await mess.reply(f"Ushbu habar yoki quyidagi link orqali botni ulashishingiz mumkin link orqali har bir ro'yxatdan o'tgan foydalanuvchi uchun {get_setting('add_man_uc')} uc beriladi!")
    elif m.text == "Chiqarish✅":
        await m.answer(f"Sizda {get_uc(m.from_user.id)} uc mavjud.")
        if int(get_uc(m.from_user.id))>get_setting("min_release_uc"):
            await m.answer(f"Hisobingizdagi uc larni chiqarib olish uchun UC Chiqarish tugmasini bosing!", reply_markup=keyboardbutton(["UC Chiqarish", "Orqaga"]))
            await User_state.get_uc.set()
        else:
            await m.answer(f"Hisobdagi uc larni chiqarib olishning minimal miqdor {get_setting('min_release_uc')} uc ga teng!")
    elif m.text == "Bot haqida🤖":
        await m.answer(get_latest_contact_message())
    elif m.text == "Takliflar🫂":
        await m.answer(f"Siz taklif qilgan havola orqali {get_invite(m.from_user.id)} nafar foydalanuvchi ro'yxatdan o'tgan!")
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Taklif qilish📣", "Chiqarish✅", "Takliflar🫂", "Bot haqida🤖"]))
        await User_state.main_menu.set()


async def user_get_pubg_id(m: m, state: s):
    if m.text == "Orqaga":
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Taklif qilish📣", "Chiqarish✅", "Takliflar🫂", "Bot haqida🤖"]))
        await User_state.main_menu.set()
    elif m.text == "UC Chiqarish":
        await m.answer("Hisobingizdagi uc ni chiqarish uchun PUBG id kiriting:", reply_markup=keyboardbutton(["Orqaga"]))


async def user_get_uc(m: m, state: s):
    if m.text == "Orqaga":
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Taklif qilish📣", "Chiqarish✅", "Takliflar🫂", "Bot haqida🤖"]))
        await User_state.main_menu.set()
    elif m.text == "UC Chiqarish":
        await bot.send_message(ADMIN_ID, f"PUBG ID: {m.text},\nUC: {get_uc(m.from_user.id)}\nTG_ID: {m.from_user.id}")
        update_uc(m.from_user.id, 0)
        await m.answer("Hisobingizdagi uc ni chiqarish uchun adminga habar yuborildi tez orada uc PUBG hisobingizga tashlab beriladi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Taklif qilish📣", "Chiqarish✅", "Takliflar🫂", "Bot haqida🤖"]))
        await User_state.main_menu.set()
