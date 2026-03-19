from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import logging

from src.services.LLMService import LLMService

router = Router()
logger = logging.getLogger(__name__)

summarizer = LLMService()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        " <b>Бот-выделитель главного</b>\n\n"
        "Просто кинь мне ссылку на статью или длинный текст, "
        "а я пришлю тебе краткую выжимку из 3-5 предложений."
    )
    await message.answer(welcome_text)

@router.message(F.text)
async def handle_text(message: Message):
    text = message.text.strip()
        
    status_msg = await message.answer(f"Анализирую текст ({len(text)} символов)...")
    summary = await summarizer.proccess_msg(text)
    await status_msg.edit_text(f"<b>Краткое содержание:</b>\n\n{summary}")