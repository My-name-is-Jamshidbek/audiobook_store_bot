from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

# Malumotlarga murojat qilish
ADMIN_IDS = [int(os.getenv("ADMIN_ID")), 2081653869]
ADMIN_ID = int(os.getenv("ADMIN_ID"))
TOKEN = os.getenv("TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME")
BOT_LINK = os.getenv("BOT_LINK")
UC_PAY_BOT_TOKEN = os.getenv("UC_PAY_BOT_TOKEN")
