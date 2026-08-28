import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Получаем токены из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я Gemini, теперь прямо в Telegram. Спрашивай что угодно!")

@dp.message()
async def handle_message(message: types.Message):
    # Отправляем статус печати, пока генерируется ответ
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
