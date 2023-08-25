"""
user app
"""
from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.keyboardbuttons import keyboardbutton
from buttons.inlinekeyboardbuttons import inlinekeyboardbutton, get_group_link_button
from database.database import *
from loader import bot
from states import *
from .payment_helper import get_price_label
from config import ADMIN_IDS

user_data = {}

async def user_main_menu(m: m, state: s):
    if m.text == "Audioteka 🎧":
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text == "Audiokitoblarim 💽":
        if len(get_user_premium_books(m.from_user.id)+get_user_premium_audiobooks(m.from_user.id)):
            await m.answer("Siz xarid qilgan audiokitoblar ro'yxati:", reply_markup=keyboardbutton(list(set(get_user_premium_books(m.from_user.id)+get_user_premium_audiobooks(m.from_user.id)))+["Chiqish"]))
            await User_state.audiobooks.set()
        else:
            await m.answer("Sizda hozircha premium kitoblar mavjud emas!")
    elif m.text == "Biz bilan aloqa 📞":
        await m.answer(get_latest_contact_message())
    elif m.text == "Qidirish🔍":
        await m.answer("Qidirish uchun kalit so'zni kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await User_state.search_books.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        await User_state.main_menu.set()


async def user_audiobooks(m: m, state:s):
    data = await state.get_data()
    # add_user_premium_audiobook(m.from_user.id, get_premium_book_id("Dunyoning ishlari"))
    # add_user_premium_book(m.from_user.id, get_premium_book_id("Dunyoning ishlari"))
    if m.text == "Chiqish":
        await m.answer("Chiqildi")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        await User_state.main_menu.set()
    elif m.text in get_user_premium_audiobooks(m.from_user.id):
        r_m = f"{get_premium_audiobook_description(m.text)}\n\n💰Audiokitob narxi - {get_premium_audiobook_price(book_name=m.text)} soʻm"
        audios = get_premium_audiobook_address(m.text)
        await m.answer_photo(
            photo=InputFile(get_premium_audiobook_photo(m.text)),
            caption=r_m,
            reply_markup=get_group_link_button(audios))
        
    elif m.text in get_user_premium_books(m.from_user.id):
        r_m = f"{get_premium_book_description(book_name=m.text)}\n\n💰Asar narxi - {get_premium_book_price(book_name=m.text)} soʻm"
        audios = get_premium_book_address(m.text)
        await m.answer_photo(
            photo=InputFile(get_premium_book_photo(book_name=m.text)),
            caption=r_m,
            reply_markup=get_group_link_button(audios))
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        await User_state.main_menu.set()


async def search_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(
                           ["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
        await User_state.main_menu.set()
    else:
        keyword = m.text
        result = search_book(keyword)
        if result:
            await m.answer("Natijalar:")
            f, n = f"", 0
            for book in result:
                n+=1
                f += f"\n{n}. {book[1]}  "
                if book[2].isdigit():
                    f+=f" Premium"
                else:
                    f+=f" Beepul"
            await m.answer(f)
        else:
            await m.answer("Kitob topilmadi.")
        await m.answer("Qidirish uchun kalit so'z yuborishingiz mumkin:")


async def user_audiobook_type(m: m, state: s):
    if m.text == "Premium audiokitoblar 💰":
        await m.answer("Premium audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Chiqish"]))
        await User_state.premium_books.set()
    elif m.text == "Bepul audiokitoblar 🎁":
        await m.answer("Beepul audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_free_books()+["Chiqish"]))
        await User_state.free_books.set()
    elif m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
        await User_state.main_menu.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Kerakli menyuni tanlashingiz mumkin:",reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Biz bilan aloqa 📞", "Qidirish🔍"]))
        await User_state.main_menu.set()


async def user_premium_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text in get_premium_books():
        await state.update_data(menu_name="premium")
        await state.update_data(premium_book_name=m.text)
        await m.answer("Kerakli menyuni tanlang:",
                reply_markup=keyboardbutton(["📔 Audio va elektron format 🎧", " Audio format 🎧", "Chiqish"]))
        data = await state.get_data()
        user_data[m.from_user.id] = data
        await state.finish()
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    

async def user_book_type(m: m, state: s):
    try:
        data = user_data[m.from_user.id]
        if m.text == "📔 Audio va elektron format 🎧":
            if data.get("premium_book_name") in get_user_premium_audiobooks(m.from_user.id):
                await m.answer("Siz ushbu kitobni allaqachon harid qilgansiz uni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin")
            else:
                r_m = f"{get_premium_audiobook_description(data.get('premium_book_name'))}\n\n💰Audiokitob narxi - {get_premium_audiobook_price(book_name=data.get('premium_book_name'))} soʻm"
                await m.answer_photo(
                    photo=InputFile(get_premium_audiobook_photo(data.get('premium_book_name'))),
                    caption=r_m,
                    reply_markup=inlinekeyboardbutton([
                        {"text": "Click", "data": f"click_{get_premium_book_id(data.get('premium_book_name'))}_a"},
                        {"text": "Payme", "data": f"payme_{get_premium_book_id(data.get('premium_book_name'))}_a"},
                        {"text": "Qo'shimcha to'lov usuli", "data": f"visa_{get_premium_book_id(data.get('premium_book_name'))}_a"},
                        ]))
                await state.finish()
        elif m.text == "Audio format 🎧":
            if data.get("premium_book_name") in get_user_premium_books(m.from_user.id):
                await m.answer("Siz ushbu kitobni allaqachon harid qilgansiz uni \"Audiokitoblarim 💽\" bo'limidan topishingiz mumkin")
            else:
                r_m = f"{get_premium_book_description(book_name=data.get('premium_book_name'))}\n\n💰Asar narxi - {get_premium_book_price(book_name=data.get('premium_book_name'))} soʻm"
                await m.answer_photo(
                    photo=InputFile(get_premium_book_photo(book_name=data.get('premium_book_name'))),
                    caption=r_m,
                    reply_markup=inlinekeyboardbutton([
                        {"text": "Click", "data": f"click_{get_premium_book_id(data.get('premium_book_name'))}_e"},
                        {"text": "Payme", "data": f"payme_{get_premium_book_id(data.get('premium_book_name'))}_e"},
                        {"text": "Qo'shimcha to'lov usuli", "data": f"visa_{get_premium_book_id(data.get('premium_book_name'))}_e"},
                        ]))
                await state.finish()
        elif m.text == "Chiqish":
            if data.get("menu_name") == "premium":
                await m.answer("Chiqildi!")
                await m.answer("Premium audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_premium_books()+["Chiqish"]))
                await User_state.premium_books.set()
            else:
                await m.answer("Siz xarid qilgan audiokitoblar ro'yxati:", reply_markup=keyboardbutton(get_user_premium_books(m.from_user.id)+["Chiqish"]))
                await User_state.audiobooks.set()        
        else:
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
                    await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                                reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
                    await User_state.main_menu.set()
                else:
                    await m.answer("Assalomu alaykum! Hush kelibsiz, muhtaram vatandosh! \n\nSiz bu bot yordamida Omar Xalil "
                                "ijrosidagi hali oʻzbek tiliga tarjima qilinmagan eng sara va noyob kitoblarning audio "
                                "va elektron formatlarini harid qilib eshitishingiz mumkin. \n\nBiz bilan birga boʻlganingiz"
                                " uchun minnatdormiz! Sizni hali koʻplab foydali manbalar bilan siylay olishimizga ishonamiz"
                                ".", reply_markup=keyboardbutton(["Ro'yxatdan o'tish"]))
                    await User_state.register.set()
    except Exception as e:
        # print(e)
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
                await m.answer("Kerakli menyuni tanlashingiz mumkin:",
                            reply_markup=keyboardbutton(["Audioteka 🎧", "Audiokitoblarim 💽", "Qidirish🔍", "Biz bilan aloqa 📞"]))
                await User_state.main_menu.set()
            else:
                await m.answer("Assalomu alaykum! Hush kelibsiz, muhtaram vatandosh! \n\nSiz bu bot yordamida Omar Xalil "
                            "ijrosidagi hali oʻzbek tiliga tarjima qilinmagan eng sara va noyob kitoblarning audio "
                            "va elektron formatlarini harid qilib eshitishingiz mumkin. \n\nBiz bilan birga boʻlganingiz"
                            " uchun minnatdormiz! Sizni hali koʻplab foydali manbalar bilan siylay olishimizga ishonamiz"
                            ".", reply_markup=keyboardbutton(["Ro'yxatdan o'tish"]))
                await User_state.register.set()


async def user_free_books(m: m, state: s):
    if m.text == "Chiqish":
        await m.answer("Chiqildi!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()
    elif m.text in get_free_books():
        audios = get_free_book_address(m.text)
        await m.answer_photo(
                        photo=InputFile(get_free_book_photo(m.text)),
                        caption=f"{get_free_book_description(m.text)}\n",
                        reply_markup=get_group_link_button(audios))
    else:
        await m.answer("Bunday menyu mavjud emas!")
        await m.answer("Audiokitob turini tanlang:", reply_markup=keyboardbutton(["Premium audiokitoblar 💰", "Bepul audiokitoblar 🎁", "Chiqish"]))
        await User_state.audiobook_type.set()

