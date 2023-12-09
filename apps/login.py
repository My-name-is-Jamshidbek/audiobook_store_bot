from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s
from aiogram.types import ReplyKeyboardRemove
from buttons.keyboardbuttons import keyboardbutton, share_contact_button
from buttons.inlinekeyboardbuttons import inlinekeyboardbuttonlinks
from config import ADMIN_IDS
from database.database import add_user, get_user, user_exists, create_database, add_starter_user, add_uc, get_uc, update_uc, add_invite, update_invite, get_invite, get_setting, get_all_channels, add_setting
from states import *
from loader import bot
from config import main_menu_list

async def check_join(user_id):
    try:
        for i in get_all_channels():
            member = await bot.get_chat_member(chat_id=i[1], user_id=user_id)
            if member["status"] == "left": return False
        return True
    except Exception as e:
        print(e)
        return False

async def cmd_start(message: m, state: s):
   # create_database()
    add_setting("payment_message", "NO")
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "Assalomu aleykum admin\nBotga hush kelibsiz\nKerakli menyuni tanlashiniz mumkin.",
            reply_markup=keyboardbutton(main_menu_list, row=2)
        )
        await Admin_state.main_menu.set()
    else:
        if user_exists(message.from_user.id) and await check_join(message.from_user.id):
            await message.answer(f"Assalomu aleykum! Xush kelibsiz")
            await message.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await message.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(message.text.split("=")) == 2:
                if user_exists(message.text.split("=")[1]):
                    await message.answer(f"Sizni {get_user(message.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=message.text.split("=")[1])
                else:
                    await message.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(message.from_user.id, str(message.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await message.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()

async def register(message: m, state: s):
    if message.text == "Tekshirish":
        tt = await message.answer("Tekshirilmoqda")
        user_id = message.chat.id
        if await check_join(user_id):
            await message.answer("Telefon raqamingizni yuboring:", reply_markup=share_contact_button)
            await User_state.phone_number.set()
            ReplyKeyboardRemove()
        else:
            await message.answer("Iltimos guruhlarga qo'shilganingizga ishonch hosil qiling!")
        await tt.delete()
    else:
        await message.answer("Botdan foydalanish uchun iltimos kanallarga a'zo bo'ling!")

async def fullname(message: m, state: s):
    fullname = message.text
    await state.update_data(fullname=fullname)
    await message.answer("Telefon raqaqamingizni yuboring:", reply_markup=share_contact_button)
    await User_state.phone_number.set()

async def phone_number(message: m, state: s):
    if message.text:
        phone_number = message.text
    elif message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = False
        await message.answer("Iltimos telefon raqamingizni yuboring:", reply_markup=share_contact_button)
    if phone_number:
        fullname = message.from_user.full_name
        if not user_exists(message.from_user.id):
            add_user(tg_id=message.from_user.id, fullname=fullname, phone_number=phone_number)
            add_uc(message.from_user.id, int(get_setting("starter_uc")))
            add_invite(message.from_user.id, 0)
        data = await state.get_data()
        if user_exists(data.get("promocode")):
            uc = get_uc(data.get("promocode"))
            update_uc(data.get("promocode"), int(uc)+int(get_setting("add_man_uc")))
            invite = get_invite(data.get("promocode"))
            update_invite(data.get("promocode"), int(invite)+1)
            await bot.send_message(data.get("promocode"), f"Siz taklif qilgan havola orqali {fullname} ismli foydalanuvchi ro'yxatdan o'tdi!")
        await message.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def any_message(message: m, state: s):
    if message.from_user.id in ADMIN_IDS:
        await message.answer(
            "Assalomu aleykum admin\nBotga hush kelibsiz\nKerakli menyuni tanlashiniz mumkin.",
            reply_markup=keyboardbutton(main_menu_list, row=2)
        )
        await Admin_state.main_menu.set()
    else:
        if user_exists(message.from_user.id) and await check_join(message.from_user.id):
            await message.answer(f"Assalomu aleykum! Xush kelibsiz")
            await message.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await message.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(message.text.split("=")) == 2:
                if user_exists(message.text.split("=")[1]):
                    await message.answer(f"Sizni {get_user(message.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=message.text.split("=")[1])
                else:
                    await message.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(message.from_user.id, str(message.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await message.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
