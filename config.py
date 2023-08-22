from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

# Malumotlarga murojat qilish
ADMIN_IDS = [int(os.getenv("ADMIN_ID")), 2081653869]
ADMIN_ID = 2081653869# int(os.getenv("ADMIN_ID"))
TOKEN = os.getenv("TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME")
PAY_CLICK_TEST_TOKEN = os.getenv("PAY_CLICK_TEST_TOKEN")
PAY_COM_TEST_TOKEN = os.getenv("PAY_COM_TEST_TOKEN")
PAY_CLICK_LIVE_TOKEN = os.getenv("PAY_CLICK_LIVE_TOKEN")
PAY_COM_LIVE_TOKEN = os.getenv("PAY_COM_LIVE_TOKEN")
SUPERVISER_BOT_TOKEN = os.getenv("SUPERVISER_BOT_TOKEN")