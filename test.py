from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

API_TOKEN = '5346182572:AAEHTGamseEg1_VQk38rXq1ptI01uZm65kY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    # Jo'natilgan foto haqidagi ma'lumotlarni olish
    photo = message.photo[-1]  # Eng katta keltirilgan foto

    # Photo ning file_id sini olish
    file_id = photo.file_id

    # File ning ma'lumotlarini olish
    file = await bot.get_file(file_id)

    # URL ni olish
    photo_url = file.file_path
    await message.reply(text=photo_url)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
