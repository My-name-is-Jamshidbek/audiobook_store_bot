from aiogram.types import Message as m, ChatPermissions
from loader import bot

async def new_chat_member(message: m):
    new_member = message.new_chat_members[0]
    user_mention = new_member.get_mention(as_html=True)
    chat_id = message.chat.id
    user_id = message.from_user.id
        
    welcome_message = f"Salom, {user_mention}! Guruhga xush kelibsiz."
    
    await bot.restrict_chat_member(chat_id, user_id, ChatPermissions())
        
    await message.reply(welcome_message)