import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения
BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Отсутствует токен бота. Установите переменную окружения BOT_TOKEN.")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/userinfo")],
        [KeyboardButton(text="/help"), KeyboardButton(text="/about")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я ваш помощник в Telegram. Используйте меню ниже для работы со мной.", 
        reply_markup=keyboard
    )

# Обработчик команды /userinfo
@router.message(Command("userinfo"))
async def userinfo_handler(message: Message):
    user = message.from_user
    premium_status = "✅ Да" if user.is_premium else "❌ Нет"
    account_type = "🤖 Бот" if user.is_bot else "👤 Пользователь"

    await message.answer(
        f"🆔 ID: {user.id}\n"
        f"👤 Имя: {user.first_name}\n"
        f"👥 Фамилия: {user.last_name or 'Не указано'}\n"
        f"🌍 Язык: {user.language_code or 'Не указано'}\n"
        f"💎 Премиум: {premium_status}\n"
        f"📌 Тип аккаунта: {account_type}"
    )

# Обработчик команды /help
@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📌 Доступные команды:\n"
        "🔹 /userinfo - Получить информацию о вашем аккаунте\n"
        "🔹 /about - О боте\n"
        "🔹 /help - Список команд"
    )

# Обработчик команды /about
@router.message(Command("about"))
async def about_handler(message: Message):
    await message.answer(
        "-Этот бот создан, чтобы упростить вашу работу в Telegram.\n"
        "-Вы можете получить информацию о себе\n"
        "-Если у вас есть идеи по улучшению, пишите разработчику!"
    )

# Основная функция запуска бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())
