from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import aiosqlite
import asyncio

API_TOKEN = 'Your API'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



async def NewTable():
    # Создание подключения к базе данных (асинхронно)
    async with aiosqlite.connect('bot_database.db') as db:
        # Создание таблицы пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT
            )
        ''')
        # Подтверждение изменений
        await db.commit()

 


keyboard = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text="Список серверов", callback_data="button1")
keyboard.add(button)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(
        message.chat.id,
        """Привет! Я бот для удалённого управления сервером Minecraft!
Через меня, ты можешь запускать и останавливать свой сервер в Minecraft,  а также вводить команды в консоль команды и смотреть онлайн сервера!
Что бы продолжить, выбери один из предложенных вариантов кнопок""",
        reply_markup=keyboard)

    #Создание таблица базы данных, если её нет
    await NewTable()    

    #Перенос ID и UserName в переменные
    user_id = message.from_user.id
    username = message.from_user.username

    #Вызов базы данных
    async with aiosqlite.connect('bot_database.db') as db:
        # Сохранение данных пользователя в базу
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
        ''', (user_id, username))
        # Подтверждение изменений
        await db.commit()

keyboard2 = InlineKeyboardMarkup(row_width=1)
button2 = InlineKeyboardButton(text='Голодные игры', callback_data="btn1")
keyboard2.add(button2)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button(callback_query: types.CallbackQuery):
    # Отвечаем на callback (обязательно)
    await bot.answer_callback_query(callback_query.id)
    
    # Изменяем сообщение
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выберите один из уже существующих серверов или создайте новый",
        reply_markup=keyboard2
    )


async def main():
    await dp.start_polling()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

