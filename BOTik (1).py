from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import sqlite3
import atexit

API_TOKEN = '7801123648:AAHX0_w3EF3_2Z4XlXjH5BFfjD0L4EBH2aA'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN,)
dp = Dispatcher()

# Подключение к базе данных
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
''')
conn.commit()

# Создание клавиатуры
builder = InlineKeyboardBuilder()
builder.add(InlineKeyboardButton(text="Список серверов", callback_data="button1"))

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        """Привет! Я бот для удалённого управления сервером Minecraft!
        Через меня, ты можешь запускать и останавливать свой сервер в Minecraft, а также вводить команды в консоль команды и смотреть онлайн сервера!
        Что бы продолжить, выбери один из предложенных вариантов кнопок""",
        reply_markup=builder.as_markup()
    )
    
    user_id = message.from_user.id
    username = message.from_user.username

    # Сохранение данных пользователя в базу
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()

# Создание второй клавиатуры
builder2 = InlineKeyboardBuilder()
builder2.add(InlineKeyboardButton(text='Голодные игры', callback_data="btn1"))

@dp.callback_query(lambda c: c.data == 'button1')
async def process_callback_button(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    await callback_query.message.edit_text(
        "Выберите один из уже существующих серверов или создайте новый",
        reply_markup=builder2.as_markup()
    )

# Закрытие соединения с базой при завершении работы
@atexit.register
def close_db():
    conn.close()

async def on_startup(bot: Bot):
    # Логика, которая выполняется при запуске бота
    pass

async def on_shutdown(bot: Bot):
    # Логика, которая выполняется при завершении работы бота
    pass

if __name__ == '__main__':
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
