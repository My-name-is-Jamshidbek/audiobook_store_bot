from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
from aiogram.types import ContentType as ct
import logging

from database.database import get_all_premium_audiobook_address, get_all_premium_book_address, get_user_premium_books_address, get_user_premium_audiobooks_address
from config import ADMIN_ID, ADMIN_IDS, SUPERVISER_BOT_TOKEN

# Bot tokenini quyidagi o'zgaruvchiga o'zgartiring
TOKEN = SUPERVISER_BOT_TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(content_types=[ct.TEXT, ct.NEW_CHAT_MEMBERS])
async def usermanager(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        chat_info = await bot.get_chat(chat_id)
        chat_invite_link = chat_info.invite_link
    except:
        pass
    if message.from_user.id not in ADMIN_IDS:
        if chat_invite_link in get_all_premium_audiobook_address()+get_all_premium_book_address():
            if chat_invite_link not in get_user_premium_audiobooks_address(user_id) and chat_invite_link not in get_user_premium_books_address(user_id):        
                try:
                    await bot.unban_chat_member(chat_id, user_id, types.ChatPermissions())
                except Exception as e:
                    await bot.send_message(ADMIN_ID, f"Guruhdan chetlatishda xatolik!\nGuruh: {chat_invite_link}\nFoydalanuvchi: {message.from_user.full_name}\nID: {user_id}\nXatolik: {e}")
            user_id = message.from_user.id
        await message.delete()    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

