import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS")
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_MAIL = os.getenv("TEST_MAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")