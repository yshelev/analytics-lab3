import os

from dotenv import load_dotenv

load_dotenv()

class Config: 
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")