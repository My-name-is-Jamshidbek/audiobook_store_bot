# """
# apps
# """
from loader import bot, dp
from buttons import *
from database import *
from states import *
from config import vote_text, BOT_LINK, chat_id, msg_id

from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types
import random
from aiogram.types import ReplyKeyboardRemove

def generate_random_numbers():
    random_numbers = ""
    for _ in range(4):
        random_numbers+=str(random.randint(1, 10))
    return random_numbers

admin_main_menu_list = [
    "Channels",
    "Voters",
    'Users',
    'Message',
]

async def check_join(user_id):
    try:
        for i in read_channels():
            member = await bot.get_chat_member(chat_id=i["link"], user_id=user_id)
            if member["status"] == "left": return False
        return True
    except Exception as e:
        print(e)
        return False
    
# start
@dp.message_handler(CommandStart())
async def start(message: types.Message, state: FSMContext):
    """

    :param message:
    """
    # print(msg)
    # print(message.text.split() =/= 2)
    if message.from_user.id == int(ADMIN_ID):
        await message.answer("The admin page is open!")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        if check_exist_user(message.from_user.id):
            await message.answer("Siz muvaffaqiyatli ovoz bergansiz.")
            # await message.answer(vote_text, reply_markup=inlinekeyboardbuttonlinks([{"text":i["name"]+" "+str(i["votes"]), "link":f"{BOT_LINK}?start="+i["name"]} for i in read_vooters()]))
            # await User.vote.set()
        elif await check_join(message.from_user.id) and len(message.text.split()) == 2 and message.text.split()[1] in [i["name"] for i in read_vooters()]:
            g_number = generate_random_numbers()
            await message.answer(f"Ushbu sonni botga yuboring: 👉🏼 {g_number}")
            await state.update_data(g_number = str(g_number))
            await state.update_data(v_number = message.text.split()[1])
            await User.number.set()
        elif await check_join(message.from_user.id):
            await message.answer("Siz muvaffaqiyatli ro'yxatda o'tgansiz, ovoz berishingiz mumkin.", reply_markup=ReplyKeyboardRemove())
            await message.answer(vote_text, reply_markup=inlinekeyboardbuttonlinks([{"text":i["name"]+" "+str(i["votes"]), "link":f"{BOT_LINK}?start="+i["name"]} for i in read_vooters()]))
            # await User.vote.set()
        else:
            links = [{"text": i["name"], "link": f"https://t.me/{i['link']}"} for i in read_channels()]
            await message.answer("Assalomu aleykum ovoz berish uchun quyidagi kanallarga a'zo bo'ling", reply_markup=inlinekeyboardbuttonlinks(links))
            await message.answer("A`zo bo'lgach \"Tekshirish\" tugmasini bosing", reply_markup=keyboardbutton(["Tekshirish"]))
            await User.login.set()                    
        await message.delete()

@dp.message_handler(state=User.number, content_types=types.ContentTypes.TEXT)
async def user_login(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if check_exist_user(message.from_user.id):
        await message.answer("Siz muvaffaqiyatli ovoz bergansiz.")
    elif str(message.text) == data.get("g_number"):
        add_a_vote(data.get("v_number"))
        add_user(message.from_user.id, data.get("v_number"))
        await message.answer(f"Siz {data.get('v_number')} ga muvaffaqiyatli ovoz berdingiz.")
    else:
        await message.answer("Iltimos raqamni to'g'ri kiriting!")

@dp.message_handler(state=User.login, content_types=types.ContentTypes.TEXT)
async def user_login(message: types.Message, state: FSMContext):
    if message.text == "Tekshirish" and await check_join(message.chat.id):
            await message.answer(vote_text, reply_markup=inlinekeyboardbuttonlinks([{"text":i["name"]+" "+str(i["votes"]), "link":f"{BOT_LINK}?start="+i["name"]} for i in read_vooters()]))
            await message.answer("Siz muvaffaqiyatli ro'yxatda o'tdingiz, ovoz berishingiz mumkin.")
            # await User.vote.set()
    else:
        await message.answer("Iltimos kanallarga a'zo bo'ling!")        
            
@dp.message_handler(state=Admin.main, content_types=types.ContentTypes.TEXT)
async def admin_main(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Channels':
        channels = read_channels()
        if channels:
            ch = ""
            for i in channels: ch+='Name: ' + i['name'] + ' Link: ' + i['link'] + '\n'
            await message.answer(f"List of available channels:", reply_markup=keyboardbutton(['Add', 'Remove', 'Back']))
            await message.answer(ch)
        else:
            await message.answer("No channels available!", reply_markup=keyboardbutton(['Add', 'Back']))
        await Admin.channels_menu.set()
    elif message.text == 'Voters':
        vooters = read_vooters()
        if vooters:
            ch = ""
            for i in vooters: ch+='Name: ' + i['name'] + ' Votes: ' + str(i['votes']) + '\n'
            await message.answer(f"List of available voters:", reply_markup=keyboardbutton(['Add', 'Remove', 'Back']))
            await message.answer(ch)
        else:
            await message.answer("No voters available!", reply_markup=keyboardbutton(['Add', 'Back']))
        await Admin.voters_menu.set()
    elif message.text == 'Users':
        await message.answer(f"Total number of users: {await users_count()}")
    elif message.text == "Message":
        await message.answer(vote_text, reply_markup=inlinekeyboardbuttonlinks([{"text":i["name"]+" "+str(i["votes"]), "link":f"{BOT_LINK}?start="+i["name"]} for i in read_vooters()]))
        
@dp.message_handler(state=Admin.voters_menu, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Add':
        await message.answer("Enter a voter name", reply_markup=keyboardbutton(['Back']))
        await Admin.voters_create.set()
    if message.text == 'Remove':
        await message.answer("Select one of the voters", reply_markup=keyboardbutton([i["name"] for i in read_voters()]+["Back"]))
        await Admin.voters_delete.set()
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

@dp.message_handler(state=Admin.voters_delete, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif message.text in [i["name"] for i in read_vooters()]:
        delete_voter(message.text)
        await message.answer("Voter removed successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

@dp.message_handler(state=Admin.voters_create, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        create_vooter(message.text)
        await message.answer("Voter added successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    
@dp.message_handler(state=Admin.channels_menu, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Add':
        await message.answer("Enter a channel name", reply_markup=keyboardbutton(['Back']))
        await Admin.channels_create.set()
    if message.text == 'Remove':
        await message.answer("Select one of the channels", reply_markup=keyboardbutton([i["name"] for i in read_channels()]+["Back"]))
        await Admin.channels_delete.set()
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

@dp.message_handler(state=Admin.channels_delete, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    elif message.text in [i["name"] for i in read_channels()]:
        delete_channel(message.text)
        await message.answer("Channel removed successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()

@dp.message_handler(state=Admin.channels_create, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        await state.update_data(channel_add=message.text)
        await message.answer("Enter the channel address", reply_markup=keyboardbutton(['Back']))
        await Admin.channels_create1.set()        

@dp.message_handler(state=Admin.channels_create1, content_types=types.ContentTypes.TEXT)
async def admin_channels_menu(message: types.Message, state: FSMContext):
    """
    :param message:
    :param state:
    """
    if message.text == 'Back':
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()
    else:
        data = await state.get_data()
        create_channel(name=data["channel_add"],link=message.text)
        await message.answer("Channel added successfully")
        await message.answer("Select the desired menu.", reply_markup=keyboardbutton(admin_main_menu_list))
        await Admin.main.set()


# # qolgan matnlar
# @dp.message_handler()
# async def els(message: types.Message):
#     """
#     :param message:
#     """
#     if database_user_table_retrieve_time_data(telegram_id=message.from_user.id) is not None:
#         m = database_user_table_retrieve_time_data(message.from_user.id)
#         await message.answer("Sana: " + m[0])
#         await message.answer('Hafta kunini tanlang:', reply_markup=hafta_kunlari)
#         await User.kun.set()
#     else:
#         await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#         await User.username.set()


# @dp.message_handler(state=User.username, content_types=types.ContentType.TEXT)
# async def username(message: types.Message, state: FSMContext):
#     """
#     :param message:
#     :param state:
#     """
#     if message.text == '👨🏻‍💻Konsultatsiya👨🏻‍💻':
#         await message.answer(f"Admin: t.me/mal_un")
#         await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#         await User.username.set()
#     elif message.text == '👨‍💻Dasturchi👨‍💻':
#         await message.answer(f"Jamshidbek Ollanazarov: t.me/mal_un")
#         await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#         await User.username.set()
#     else:
#         try:
#             int(message.text)
#             await state.update_data(studentuser=message.text)
#             await message.answer('Student parolingizni kriting:')
#             await User.parol.set()
#         except Exception as _:
#             await message.answer('Student id noto`g`ri!')
#             await User.username.set()


# @dp.message_handler(state=User.parol, content_types=types.ContentType.TEXT)
# async def davomatga(message: types.Message, state: FSMContext):
#     """
#     :param message:
#     :param state:
#     """
#     if message.text == '👨🏻‍💻Konsultatsiya👨🏻‍💻':
#         await message.answer(f"Admin: t.me/mal_un")
#         await message.answer('Student parolingizni kriting:')
#         await User.parol.set()
#     elif message.text == '👨‍💻Dasturchi👨‍💻':
#         await message.answer(f"Jamshidbek Ollanazarov: t.me/mal_un")
#         await message.answer('Student parolingizni kriting:')
#         await User.parol.set()
#     else:
#         user = await state.get_data()
#         user = user.get('studentuser')
#         await bot.delete_message(message.from_user.id,message.message_id)
#         msgid = await message.answer('Tekshirilmoqda...')
#         students_schedule_r = students_schedule(password=message.text, username=user, telegram_id=message.from_user.id)
#         if students_schedule_r['result']:
#             database_user_add_data(
#                 telegram_id=message.from_user.id,
#                 student_id=user,
#                 student_password=message.text,
#                 student_about=students_schedule_r['reason']
#             )
#             await state.update_data(parol=message.text)
#             await bot.delete_message(chat_id=message.from_user.id, message_id=msgid.message_id)
#             await message.answer(students_schedule_r['reason'])
#             await message.answer('Hafta kunini tanlang:', reply_markup=hafta_kunlari)
#             await User.kun.set()
#         else:
#             await bot.delete_message(chat_id=message.from_user.id, message_id=msgid.message_id)
#             await message.answer('Student parol yoki id xato!')
#             await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#             await User.username.set()


# @dp.message_handler(state=User.kun, content_types=types.ContentType.TEXT)
# async def haftalar(message: types.Message):
#     """
#     :param message:
#     """
#     if message.text == '👨🏻‍💻Konsultatsiya👨🏻‍💻':
#         await message.answer(f"Admin: t.me/mal_un")
#         await message.answer('Hafta kunini tanlang:', reply_markup=hafta_kunlari)
#         await User.kun.set()
#     elif message.text == '👨‍💻Dasturchi👨‍💻':
#         await message.answer(f"Jamshidbek Ollanazarov: t.me/mal_un")
#         await message.answer('Hafta kunini tanlang:', reply_markup=hafta_kunlari)
#         await User.kun.set()
#     elif message.text == 'Boshiga qaytish':
#         database_user_table_remove_data(message.from_user.id)
#         database_user_remove_data(message.from_user.id)
#         await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#         await User.username.set()
#     elif message.text == "Yangilash":
#         msgid = await message.answer("Yangilanmoqda...")
#         telegram_id, student_id, student_parol, about = database_user_retrieve_data(message.from_user.id)
#         database_user_table_remove_data(message.from_user.id)
#         # database_user_remove_data(message.from_user.id)
#         about = students_schedule(password=student_parol, username=student_id, telegram_id=telegram_id)
#         await bot.delete_message(chat_id=message.from_user.id, message_id=msgid.message_id)
#         await message.answer(about['reason'])
#         await message.answer('Hafta kunini tanlang:', reply_markup=hafta_kunlari)
#         await User.kun.set()
#     elif kuntek(message.text):
#         if database_user_table_retrieve_data(telegram_id=message.from_user.id, day=message.text) is not None:
#             await message.answer(database_user_table_retrieve_data(telegram_id=message.from_user.id,
#                                                                    day=message.text)[0],
#                                  reply_markup=hafta_kunlari)
#             await User.kun.set()
#         else:
#             await message.answer(
#                 text='Sizning dars jadvalingizni yangilashda xatolik yuz berdi iltimos qaytadan urinib ko`ring.')
#             await message.answer('Student id (username) ingizni kiriting:', reply_markup=keyboard_menyu_admin)
#             await User.username.set()
#     else:
#         await message.answer('Bunday kun mavjud emas!', reply_markup=hafta_kunlari)
#         await User.kun.set()
