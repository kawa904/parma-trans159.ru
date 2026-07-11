import os
from dotenv import load_dotenv

# Принудительно указываем UTF-8
load_dotenv(override=True, encoding='utf-8')

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SITE_NAME = os.getenv("SITE_NAME")
    CONTACT_PHONE = os.getenv("CONTACT_PHONE")
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
    OWNER_NAME = os.getenv("OWNER_NAME")
    OWNER_INN = os.getenv("OWNER_INN")
    OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")
    ENV = os.getenv("ENV", "development")

config = Config()