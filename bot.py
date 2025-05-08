# Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import random
import logging
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

# Настройка логирования
logging.basicConfig(level=logging.INFO)

import os
API_TOKEN = os.getenv("BOT_TOKEN")  # Токен берется из переменных Render
MY_USER_ID = int(os.getenv("MY_USER_ID"))  # ID тоже из переменных

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Список видео: file_id загруженных в Telegram видео
VIDEOS = [
    "BAACAgIAAxkBAAEBQkRg5sV4p6LZg8kJ8r1D6s6k9h_9QgACPgADVp29Cksx2U1f8KXTSIE",
    "BAACAgIAAxkBAAEBQkVg5sV7X3f9TIyR6Fq4T8n9zX1LSwACQwADVp29Cn1aKZxH5qW7SIK",
    # Добавьте свои идентификаторы
]

# Функция создания клавиатуры
def get_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️ Дальше", callback_data="next"),
            InlineKeyboardButton(text="❤️ Лайк", callback_data="like")
        ]
    ])
    return keyboard

... # Функция отправки случайного видео
async def send_random_video(chat_id: int):
    video_id = random.choice(VIDEOS)
    await bot.send_video(
        chat_id=chat_id,
        video=video_id,
        caption="Наслаждайтесь видео!",
        reply_markup=get_keyboard()
    )
... 
... # Команда /start
... @dp.message(CommandStart())
... async def cmd_start(message: Message):
...     await message.answer(
...         "Привет! Я бот-мини-ТикТок. Нажми ▶️ Дальше, чтобы посмотреть видео!",
...         reply_markup=get_keyboard()
...     )
... 
... # Callback на кнопки
... @dp.callback_query(F.data.in_({"next", "like"}))
... async def process_callback(callback_query: types.CallbackQuery):
...     if callback_query.data == "like":
...         await callback_query.answer("❤️ Лайк! Видео добавлено в избранное.")
...     else:
...         await callback_query.answer()
...     await send_random_video(callback_query.from_user.id)
... 
... # Обработчик получения file_id от разработчика
... @dp.message(F.from_user.id == MY_USER_ID, F.content_type == ContentType.VIDEO)
... async def get_file_id(message: Message):
...     await message.reply(f"📂 file_id вашего видео: `{message.video.file_id}`")
... 
... # Главная функция запуска
... async def main():
...     try:
...         await dp.start_polling(bot)
...     finally:
...         await bot.session.close()
... 
... if __name__ == "__main__":
...     asyncio.run(main())
