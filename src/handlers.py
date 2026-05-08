from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import logging
from pathlib import Path
import pandas as pd

from src.services.LLMService import LLMService
from src.config import Config

router = Router()
logger = logging.getLogger(__name__)

user_agents = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome = """ИИ-Аналитик данных (LangChain + Groq)
    
Отправь CSV или Excel — я загружу данные и подготовлю агента.
После загрузки пиши запросы:
• «Проведи полный EDA»
• «Какие пропуски в колонке Age?»
• «Найди корреляции»
• «Топ-5 инсайдов»

Агент сам пишет и выполняет Python-код!"""
    await message.answer(welcome)

@router.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    name = doc.file_name.lower()
    
    if not (name.endswith('.csv') or name.endswith('.xlsx') or name.endswith('.xls')):
        return await message.answer("Только CSV или Excel")
    
    temp_dir = Path(Config.TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / f"{message.from_user.id}_{doc.file_name}"
    
    try:
        file = await message.bot.get_file(doc.file_id)
        await message.bot.download_file(file.file_path, file_path)
    except Exception as e:
        logger.error(f"Download error: {e}")
        return await message.answer("Ошибка загрузки")
    
    try:
        if name.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        caption = message.caption or ""
        agent = LLMService()
        agent.init_agent(df, context=caption)
        
        user_agents[message.from_user.id] = agent
        
        await message.answer(
            f"Данные загружены: {df.shape[0]} × {df.shape[1]}\n"
            f"Колонки: <code>{', '.join(df.columns)}</code>\n\n"
            f"Агент готов! Пиши запрос для анализа.",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.exception("Init error")
        await message.answer(f"Ошибка инициализации: {str(e)[:500]}")
    finally:
        file_path.unlink(missing_ok=True)

@router.message(F.text)
async def handle_query(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_agents:
        return await message.answer(
            "Сначала загрузи файл с данными (CSV или Excel)"
        )
    
    agent = user_agents[user_id]
    query = message.text.strip()
    
    status = await message.answer("Агент думает...")
    
    try:
        result = await agent.analyze(query)
        
        await status.delete()
        
        output = result.get("output", "Нет результата")
        
        for i in range(0, len(output), 4000):
            part = output[i:i+4000]
            prefix = "Результат анализа:\n\n" if i == 0 else ""
            await message.answer(prefix + part)
        
        if not result.get("ok"):
            await message.answer("Анализ завершился с ошибкой. ")
            
    except Exception as e:
        logger.exception("Query error")
        await status.edit_text(f"Ошибка: {str(e)[:500]}")

@router.message(CommandStart())
async def reset_agent(message: Message):
    user_agents.pop(message.from_user.id, None)