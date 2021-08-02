import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

DEBUG = os.getenv("DEBUG", 'False') in 'True'
