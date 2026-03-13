import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler import send_daily_vocab
from llm import get_feedback

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

user_context = {}
user_ids = []

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
    await message.answer("Привет! Я буду присылать тебе слова и идиомы по расписанию.\nКогда получишь слово — составь предложение и я дам feedback!")

@dp.message(F.text & ~F.text.startswith("/"))
async def handle_sentence(message: Message):
    user_id = message.from_user.id
    if user_id not in user_context:
        await message.answer("Сначала получи слово и идиому! Жди по расписанию 😊")
        return
    ctx = user_context[user_id]
    feedback = get_feedback(ctx["word"], ctx["idiom"], message.text)
    await message.answer(feedback)

async def main():
    scheduler = AsyncIOScheduler()
    from datetime import datetime, timedelta
    run_time = datetime.now() + timedelta(minutes=1)
    print(f"Scheduled for: {run_time}")
    print(f"user_ids at start: {user_ids}")
    scheduler.add_job(
        send_daily_vocab,
        "date",
        run_date=run_time,
        args=[bot, user_ids, user_context]
    )
    scheduler.start()
    print("Scheduler started, jobs:", scheduler.get_jobs())
    print("Bot started...")
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
    await message.answer(f"Привет! Твой user_id: {user_id}")  # добавь это

if __name__ == "__main__":
    asyncio.run(main())