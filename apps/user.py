"""
user app
"""
from aiogram.types import Message as m, InputFile, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext as s
from aiogram.types import CallbackQuery
import os

from buttons.keyboardbuttons import keyboardbutton
from buttons.inlinekeyboardbuttons import create_inline_keyboard as inlinekeyboardbutton, get_group_link_button, inlinekeyboardbuttonlinks
from database.database import *
from loader import bot, pay_bot
from states import *
from apps.login import *
# from .payment_helper import get_price_label
from config import ADMIN_IDS, BOT_LINK, ADMIN_ID


async def user_main_menu(m: m, state: s):
    if m.text == "📞 Murojaat":
        await m.answer("👨🏻‍💻 Adminga murojaat qilish uchun pastdagi tugmani bosing.", reply_markup=inlinekeyboardbuttonlinks([{"text":"↗️ Bog'lanish", "link":"https://t.me/vooADMIN"}]))
    elif m.text == "📊 Statistika":
        await m.answer(f"👥 Bot foydalanuvchilari: {all_users_count()}\n\n🗣 Siz taklif qilganlar: {get_invite(m.from_user.id)}")
    elif m.text == "🏆 Top reyting":
        f = ""
        top_users = get_maximum_amount_users(limit=5)
        for index, user in enumerate(top_users, start=1):
            user_id, max_amount = user
            user_name = get_user_name_by_id(user_id)
            f+=(f"{index}. {user_name} takliflar {int(max_amount)}\n")
        await m.answer(f)
    elif m.text == "✅ Ma'lumot":
        await m.answer("🔊 Agar bizning kanalimizni ko’rmoqchi bo’lsagiz pastdagi tugamani bosing.", reply_markup=inlinekeyboardbuttonlinks([{"text":"👁️‍ Ko’rish", "link":"https://t.me/uc9953"}]))
        await m.answer("🔐 Isbot kanalimizni ko’rmoqchi bo’lsagiz pastdagi tugamani bosing.", reply_markup=inlinekeyboardbuttonlinks([{"text":"👁️‍ Ko’rish", "link":"https://t.me/uc9953isbot"}]))
        await m.answer("👨🏻‍💻Adminga murojat qilmochi bo’lsagiz pastdagi tugamni bosing.", reply_markup=inlinekeyboardbuttonlinks([{"text":"👁️‍ O'tish", "link":"https://t.me/vooADMIN"}]))
        # await m.answer(get_latest_contact_message())
    elif m.text == "💬 Fikr bildirish":
        await m.answer("🤖 Botimiz haqida o'z fikringizni yozib qoldiring.", reply_markup=keyboardbutton(["🚫 Bekor qilish"]))
        await User_state.get_thought.set()
    elif m.text == "💸 UC ishlash":
        await m.answer("💸Siz UC ishlash bo'limidasiz.", reply_markup=keyboardbutton(["🗣 Taklif qilish", "💳 Hisobim", "🆔 ID raqam kiritish", "📥 UC yechish", "🔙 Orqaga", "🔝 Asosiy Menyu"], row=2))
        await User_state.sub_menu.set()
    elif m.text == "💸 UC OLISH 💸":
        m = await m.answer("...", reply_markup=ReplyKeyboardRemove())
        data = []
        for i in get_uc_prices():
            data.append({"text": f"💵 {int(i[2])} UC ➖ {int(i[1])} so'm", "data": f"buyuc_{i[0]}"})    
        data.append({"text": "🔙Orqaga🔙", "data": "buyucbreak_"})
        _mid = await m.answer("‼️999999 ♻️Eng Arzon UC BIZDA ✔️ \n   🔔 PUBG MOBILE G.L ✅\n\n Undan ham ko’proq bo’lgan \n♾♾ olib beramiz … ✅\n\n💳 TOʻLOV CHEKI TASHLANMAGAN.    HOLATDA TOLOV 0️⃣ GA TENG ❌\n                 🔻🔻🔻🔻🔻🔻\n👨🏻‍💻 Admin: @vooALISHER\n                 🔺🔺🔺🔺🔺🔺\n\n📢  Kanal: @uc9953  ✅\n📝  Isbot: @isbotuc9953  ✅\n\n ☎️ Tel : +998 88 999 9953 ✅\n\n⤵️ O‘zingizga kerakli UC miqdorini tanlang:", reply_markup=inlinekeyboardbutton(data))
        await state.update_data(_mid=_mid.message_id)
        await m.delete()
        await User_state.buy_uc_main.set()
    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()


async def user_buy_uc(callback_query: CallbackQuery, state: s):
    data = await state.get_data()
    try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
    except Exception as _:pass
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    m = callback_query.data.split("_")
    if m[0]=="buyuc":
        await state.update_data(buy_uc_id=m[1])
        btns = [{"text": "✅To'lov qildim", "data": "check"}, {"text": "🔙Orqaga🔙", "data": "break"}]
        _mid = await bot.send_photo(callback_query.from_user.id, photo=InputFile("database/humo_logo.jpg"), caption=f"{get_setting('payment_message')}\n\n\n💸 {get_uc_amount(m[1])} UC Uchun To‘lov miqdori: {get_uc_price(m[1])} UZS💵\n📃 - PULNI TASHAGANIZ HAQIDA CHEK ESDAN CHIQMASIN ✅", reply_markup=inlinekeyboardbutton(btns))
        await state.update_data(_mid=_mid.message_id)
        await User_state.buy_uc_check.set()
    elif m[0]=="buyucbreak":
        await bot.send_message(callback_query.from_user.id, "🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_buy_check(callback_query: CallbackQuery, state: s):
    data = await state.get_data()
    try:await bot.delete_message(callback_query.from_user.id, data.get("_mid"))
    except Exception as _:pass
    await callback_query.answer()  # Yaqin kelgan so'rovni qabul qilish
    m = callback_query.data.split("_")
    if m[0]=="check":
        _mid = await bot.send_message(callback_query.from_user.id, "PUBG MOBILE ID raqamingizni kiriting \nAniqlik kiritish uchun iloji bo'lsa nik\n(tahrirlangan xabarlarga bot javob bermaydi):", reply_markup=keyboardbutton(["Orqaga qaytish 🔙"]))
        await state.update_data(_mid=_mid.message_id)
        await User_state.buy_uc_id.set()
    elif m[0]=="break":
        data = []
        for i in get_uc_prices():
            data.append({"text": f"💵 {int(i[2])} UC ➖ {int(i[1])} so'm", "data": f"buyuc_{i[0]}"})    
        data.append({"text": "🔙Orqaga🔙", "data": "buyucbreak_"})
        _mid = await bot.send_message(callback_query.from_user.id, "‼️999999 ♻️Eng Arzon UC BIZDA ✔️ \n   🔔 PUBG MOBILE G.L ✅\n\n Undan ham ko’proq bo’lgan \n♾♾ olib beramiz … ✅\n\n💳 TOʻLOV CHEKI TASHLANMAGAN.    HOLATDA TOLOV 0️⃣ GA TENG ❌\n                 🔻🔻🔻🔻🔻🔻\n👨🏻‍💻 Admin: @vooALISHER\n                 🔺🔺🔺🔺🔺🔺\n\n📢  Kanal: @uc9953  ✅\n📝  Isbot: @isbotuc9953  ✅\n\n ☎️ Tel : +998 88 999 9953 ✅\n\n⤵️ O‘zingizga kerakli UC miqdorini tanlang:", reply_markup=inlinekeyboardbutton(data))
        await state.update_data(_mid=_mid.message_id)
        await User_state.buy_uc_main.set()

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_buy_id(m: m, state: s):
    if m.text == "Orqaga qaytish 🔙":
        await bot.send_message(m.from_user.id, "🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text:
        await bot.send_message(m.from_user.id, f"ID qabul qilindi✅\nTo'lovingizni chek yoki skreenshotini shu yerga yuboring:\nTo'lov cheki tashlanmagan holatda to'lov 0 ga teng!")  
        await state.update_data(buy_uc_pubg_id=m.text)
        await User_state.buy_uc_chek.set()  

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_buy_uc_chek(m: m, state: s):
    download_dir = "database/media/"
    if m.photo:
        data = await state.get_data()
        buy_uc_id = buy_uc(data.get('buy_uc_id'), m.from_user.id)

        for photo in m.photo:
            file_id = photo.file_id
            file = await bot.download_file_by_id(file_id)
            file_path = os.path.join(download_dir, f"{file_id}.jpg")
            with open(file_path, 'wb') as new_file:
                new_file.write(file.read())
        _id = await pay_bot.send_photo(chat_id=ADMIN_ID, photo=InputFile(file_path), caption=f"ORDER ID: {buy_uc_id}")
        await pay_bot.send_message(ADMIN_ID, f"UC: {get_uc_amount(data.get('buy_uc_id'))}\nNARX: {get_uc_price(data.get('buy_uc_id'))}\nPUBG ID: {data.get('buy_uc_pubg_id')}\nORDER ID: {buy_uc_id}", reply_markup=inlinekeyboardbutton([{"text":"✅", "data":f"check_{buy_uc_id}"}, {"text":"🚫", "data":f"close_{buy_uc_id}"}]), reply_to_message_id=_id.message_id)
        
        
        await m.answer(f"Xurmatli Mijoz🤝\n\nUC sotib olish uchun bergan arizangiz qabul qilindi, ariza 5-15daqiqa ichida ko‘rib chiqiladi⚖️\nAgarda siz, Botga yolgon(fake/montaj) yo‘llar bilan Chek tashlagan bo‘lsangiz botdan ban olish ehtimolingiz bor🙌\n\nBuyurtma raqami: {buy_uc_id}")
        await bot.send_message(m.from_user.id, "🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    
    elif m.document:
        data = await state.get_data()
        buy_uc_id = buy_uc(data.get('buy_uc_id'), m.from_user.id)

        file_id = m.document.file_id
        file = await bot.download_file_by_id(file_id)
        file_path = os.path.join(download_dir, m.document.file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(file.read())
        
        _id = await pay_bot.send_document(chat_id=ADMIN_ID, document=InputFile(file_path), caption=f"ORDER ID: {buy_uc_id}")
        await pay_bot.send_message(ADMIN_ID, f"UC: {get_uc_amount(data.get('buy_uc_id'))}\nNARX: {get_uc_price(data.get('buy_uc_id'))}\nPUBG ID: {data.get('buy_uc_pubg_id')}\nORDER ID: {buy_uc_id}", reply_markup=inlinekeyboardbutton([{"text":"✅", "data":f"check_{buy_uc_id}"}, {"text":"🚫", "data":f"close_{buy_uc_id}"}]), reply_to_message_id=_id.message_id)
        
        await m.answer(f"Xurmatli Mijoz🤝\n\nUC sotib olish uchun bergan arizangiz qabul qilindi, ariza 5-15daqiqa ichida ko‘rib chiqiladi⚖️\nAgarda siz, Botga yolgon(fake/montaj) yo‘llar bilan Chek tashlagan bo‘lsangiz botdan ban olish ehtimolingiz bor🙌\n\nBuyurtma raqami: {buy_uc_id}")
        await bot.send_message(m.from_user.id, "🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    
    elif m.text:
        if m.text == "Orqaga qaytish 🔙":
            await bot.send_message(m.from_user.id, "🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        
    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        m.answer("Iltimos rasm jo'nating!")
    
async def user_sub_menu(m: m, state: s):
    if m.text in ["🔙 Orqaga", "🔝 Asosiy Menyu"]:
        await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text == "🗣 Taklif qilish":    #Men ushbu botdan
        m = await m.answer(f"Men ushbu <a href=\"{BOT_LINK}?start=taklif_id={m.from_user.id}\">botdan</a>  anchadan beri foydalanib kelaman 😍\nBot orqali uclarni tekinga ishlab olaman ✅ 100 % ishonchli 🤠\nBunga sizni ham taklif qilaman👇👇", reply_markup=inlinekeyboardbuttonlinks([{"text":"👁️‍ O'tish", "link":f"{BOT_LINK}?start=taklif_id={m.from_user.id}"}]))
        await m.reply(f"Ushbu habarni ulashish orqali do'stlaringizni taklif qilishingiz mumkin.\n\n🗣 Har bir taklif qilgan do'stingiz uchun sizga {get_setting('add_man_uc')} UC taqdim etiladi!\n\n👇🏻 Sizning refereal havolangiz: {BOT_LINK}?start=taklif_id={m.from_user.id}")
        # mess = await m.answer(f"<a href=\"{BOT_LINK}?start=taklif_id={m.from_user.id}\">Ushbu botga start bosib ro'yxatdan o'tish orqali PUBG ilovangiz uchun uc yutib oling!</a>")
        # await mess.reply(f"Ushbu habar yoki quyidagi link orqali botni ulashishingiz mumkin link orqali har bir ro'yxatdan o'tgan foydalanuvchi uchun {get_setting('add_man_uc')} uc beriladi!")
    elif m.text == "💳 Hisobim":
        await m.answer(f"💰Sizning hisobingiz: {get_uc(m.from_user.id)}\n\n👥 Sizning taklif qilgan do'stlaringiz: {get_invite(m.from_user.id)} nafar")
    elif m.text in ["🆔 ID raqam kiritish", "📥 UC yechish"]:
        await m.answer(f"💰Hisobingizda {get_uc(m.from_user.id)} uc mavjud.")
        if int(get_uc(m.from_user.id))>int(get_setting("min_release_uc")):
            await m.answer(f"Hisobingizdagi UC larni chiqarib olish uchun UC chiqarish tugmasiga bosing.", reply_markup=keyboardbutton(["💸 UC Chiqarish", "🚫 Bekor qilish"]))
            await User_state.get_uc.set()
        else:
            await m.answer(f"⁉️ Hisobdagi UC larni chiqarib olishning minimal miqdor {get_setting('min_release_uc')} UC ga teng!")

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_get_thought(m: m, state: s):
    if m.text == "🚫 Bekor qilish":
        await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text:
        await bot.send_message(ADMIN_ID, m.text)
        await m.answer("Fikr bildirganingiz uchun tashakkur.")
        await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_get_pubg_id(m: m, state: s):
    if m.text == "🚫 Bekor qilish":
        await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text == "💸 UC Chiqarish":
        await m.answer("🔹\"PUBG MOBILE\" ID raqamingizni yozib qoldiring. Barcha ishlagan UC laringizni shu ID ga chiqarib olishingiz mumkin bo'ladi.", reply_markup=keyboardbutton(["🚫 Bekor qilish"]))

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

async def user_get_uc(m: m, state: s):
    if m.text == "🚫 Bekor qilish":
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
    elif m.text:
        await bot.send_message(ADMIN_ID, f"PUBG ID: {m.text},\nUC: {get_uc(m.from_user.id)}\nTG_ID: {m.from_user.id}")
        update_uc(m.from_user.id, 0)
        await m.answer("Hisobingizdagi UC larni chiqarish uchun adminga habar yuborildi tez orada UC lar PUBG hisobingizga tashlab beriladi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()

    elif m.text == "/start":
        if user_exists(m.from_user.id) and await check_join(m.from_user.id):
            await m.answer(f"Assalomu aleykum! Xush kelibsiz")
            await m.answer("🎛 Siz asosiy menyudasiz.",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
            await User_state.main_menu.set()
        else:
            await m.answer(f"Assalomu aleykum! Hush kelibsiz", reply_markup=keyboardbutton(["Tekshirish"]))
            if len(m.text.split("=")) == 2:
                if user_exists(m.text.split("=")[1]):
                    await m.answer(f"Sizni {get_user(m.text.split('=')[1])[2]} taklif qildi. Taklif qilgan foydalanuvchiga uc sovg'a qilinishi uchun botda ro'yxatdan o'ting.")
                    await state.update_data(promocode=m.text.split("=")[1])
                else:
                    await m.answer("Promo kod noto'g'ri!")
            try:
                add_starter_user(m.from_user.id, str(m.from_user.full_name))
            except:
                pass
            links = [{"text": i[0], "link": f"https://t.me/{i[1][1:]}"} for i in get_all_channels()]
            await m.answer(f"Bot ishini davom etishi uchun quyidagi kanallarga a'zo bo'ling:", reply_markup=inlinekeyboardbuttonlinks(links))
            await User_state.register.set()
    elif m.text == "/help" or m.text == "/yordam":
        await bot.send_video(chat_id=m.chat.id, video=InputFile("/home/admin/audiobook_store_bot/database/media/IMG_7750.MOV"), caption='Uc ishlash qo’llanma 👇👇\n#start tugamasini bosig.\n1. 💸 Uc ishlash bo’limini tanlang ✅\n2. Taklif qilish tugmasini bosing ✅ \n3. Sizga berilgan havolani do’stlarigizga yuboring.✅\n4. Siz yuborgan havoladan do’stlaringiz to’liq ro’yhatdan o’tishi shart shundagina sizga belgilangan uc beriladi 🤩\n5. Uc miqdoringiz 61 uc bo’lganda uc chiqarib olishingiz munkin ✅')
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["💸 UC ishlash", "💸 UC OLISH 💸", "📊 Statistika", "🏆 Top reyting", "📞 Murojaat", "✅ Ma'lumot", "💬 Fikr bildirish"], row=2))
        await User_state.main_menu.set()
