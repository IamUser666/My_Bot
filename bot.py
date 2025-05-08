import random
import logging
import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN")
MY_USER_ID = int(os.getenv("MY_USER_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Список видео: file_id загруженных в Telegram видео
VIDEOS = [
    "BAACAgIAAxkBAAEBQkRg5sV4p6LZg8kJ8r1D6s6k9h_9QgACPgADVp29Cksx2U1f8KXTSIE",
    "BAACAgIAAxkBAAEBQkVg5sV7X3f9TIyR6Fq4T8n9zX1LSwACQwADVp29Cn1aKZxH5qW7SIK",
]

def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️ Дальше", callback_data="next"),
            InlineKeyboardButton(text="❤️ Лайк", callback_data="like")
        ]
    ])
    return keyboard

async def send_random_video(chat_id: int):
    video_id = random.choice(VIDEOS)
    await bot.send_video(
        chat_id=chat_id,
        video=video_id,
        caption="Наслаждайтесь видео!",
        reply_markup=get_keyboard()
    )
...
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-мини-ТикТок. Нажми ▶️ Дальше, чтобы посмотреть видео!",
        reply_markup=get_keyboard()
    )

@dp.callback_query(F.data.in_({"next", "like"}))
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "like":
        await callback_query.answer("❤️ Лайк! Видео добавлено в избранное.")
    else:
        await callback_query.answer()
    await send_random_video(callback_query.from_user.id)

@dp.message(F.from_user.id == MY_USER_ID, F.content_type == ContentType.VIDEO)
async def get_file_id(message: Message):
    if message.video:
        await message.reply(f"📂 file_id вашего видео: `{message.video.file_id}`")

# Минимальный HTTP-сервер
async def web_server():
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8000))  # Используйте переменную PORT
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    return runner

async def main():
    http_runner = await web_server()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await http_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
