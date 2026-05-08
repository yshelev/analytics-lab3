import os
from dotenv import load_dotenv

load_dotenv()

class Config: 
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    TEMP_DIR = "./temp"
    MODEL = "llama-3.3-70b-versatile"