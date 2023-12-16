from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

# Malumotlarga murojat qilish
ADMIN_IDS = [int(os.getenv("ADMIN_ID")), 20816538699]
ADMIN_ID = int(os.getenv("ADMIN_ID"))
TOKEN = os.getenv("TEST_TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME")
BOT_LINK = "https://t.me/buyurtma_bot_zakaz_bot"
UC_PAY_BOT_TOKEN = os.getenv("UC_PAY_BOT_TOKEN")
main_menu_list = [ "Biz bilan aloqa 📞", "Statistika 📊", "UC Chiqarish", "Boshlang'ich uc", "Odam qo'shish", "Reklama", "Kanallar", "UC narxlar", "Foydalanuvchi", "To'lov ma'lumoti"]