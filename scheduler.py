import json
import random
from aiogram import Bot

def load_data():
    with open("data/words.json", "r", encoding="utf-8") as f:
        return json.load(f)

async def send_daily_vocab(bot: Bot, user_ids: list[int], user_context: dict):
    print(f"send_daily_vocab called! user_ids: {user_ids}")
    data = load_data()
    word = random.choice(data["words"])
    idiom = random.choice(data["idioms"])

    text = (
        f"📚 *Word of the day:*\n"
        f"*{word['word']}* — {word['definition']}\n"
        f"_Example: {word['example']}_\n\n"
        f"💬 *Idiom of the day:*\n"
        f"*{idiom['idiom']}* — {idiom['definition']}\n"
        f"_Example: {idiom['example']}_\n\n"
        f"✍️ Now write a sentence using both!"
    )

    for user_id in user_ids:
        user_context[user_id] = {"word": word["word"], "idiom": idiom["idiom"]}
        await bot.send_message(user_id, text, parse_mode="Markdown")