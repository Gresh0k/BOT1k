from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import aiosqlite
import asyncio
import os
from aiogram.types import Message



API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

server_name1 = "C:\BOT1\Server\Start.bat"

DATABASE_PATH = "bot_database.db"  # Путь к твоей SQLite базе данных

ADMINS = {992729712}


@dp.message_handler(commands=["grant_access"])
async def grant_access(message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    args = message.text.split()
    if len(args) != 3:
        await message.reply("Использование: /grant_access user_id server_name")
        return

    user_id = int(args[1])
    server_name = args[2]

    await add_user_server(user_id, server_name)
    await message.reply(f"Пользователю {user_id} назначен сервер {server_name}")


async def remove_user_server(user_id: int, server_name: str):
    """Удаляет доступ пользователя только к указанному серверу."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM user_servers WHERE user_id = ? AND server_name = ?", 
            (user_id, server_name)
        )
        await db.commit()


@dp.message_handler(commands=["revoke_access"])
async def revoke_access(message: Message):
    if message.from_user.id not in ADMINS:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    args = message.text.split()
    if len(args) != 3:
        await message.reply("Использование: /revoke_access user_id server_name")
        return

    user_id = int(args[1])
    server_name = args[2]

    await remove_user_server(user_id, server_name)
    await message.reply(f"Доступ к серверу {server_name} для пользователя {user_id} был удалён.")




async def add_user_server(user_id: int, server_name: str):
    """Добавляет (или обновляет) сервер для пользователя в базе данных."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO user_servers (user_id, server_name) VALUES (?, ?)",
            (user_id, server_name),
        )
        await db.commit()



async def NewTable():
    # Создание подключения к базе данных (асинхронно)
    async with aiosqlite.connect('bot_database.db') as db:
        # Создание таблицы пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_servers (
                user_id INTEGER PRIMARY KEY,
                server_name TEXT NOT NULL
            );

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

async def add_serv():
    async def add_user_server(user_id: int, server_name: str):
        async with aiosqlite.connect("bot_database.db") as db:
            await db.execute(
                "INSERT OR REPLACE INTO user_servers (user_id, server_name) VALUES (?, ?)",
                (user_id, server_name1),
            )
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




@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def startServer(callback_query: types.CallbackQuery):
    # Отвечаем на callback (обязательно)
    await bot.answer_callback_query(callback_query.id)
    
    # Изменяем сообщение
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Сервер запускается...",
        reply_markup=keyboard2
    )
    os.startfile(server_name1)

async def main():
    await dp.start_polling()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
