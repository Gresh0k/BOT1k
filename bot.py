from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiosqlite
import psutil
import os
import subprocess
from mcrcon import MCRcon

API_TOKEN = ''

# Инициализация хранилища состояний
storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

SERVER_BAT_PATH = "start.bat"
SERVER_FOLDER = os.getcwd()

mc = MCRcon("46.147.151.48", "1488", port=25575)


async def NewTable():
    # Создание таблицы пользователей с колонкой "level"
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                level INTEGER DEFAULT 1 
            )
        ''')
        await db.commit()


async def get_user_level(user_id: int) -> int:
    # Получение уровня пользователя из базы данных
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT level FROM users WHERE user_id = ?', (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else 1  # По умолчанию уровень 1, если пользователь не найден


async def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    # Создание клавиатуры в зависимости от уровня пользователя
    user_level = await get_user_level(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    if user_level >= 1:
        keyboard.add(InlineKeyboardButton(text="Узнать свой ID", callback_data="Get_ID"))
    if user_level >= 2:
        keyboard.add(InlineKeyboardButton(text="Запустить сервер", callback_data="start_server"))
    if user_level >= 3:
        keyboard.add(InlineKeyboardButton(text="Остановить сервер", callback_data="stop_server"))
    if user_level >= 4:
        keyboard.add(InlineKeyboardButton(text="Ввести команду в консоль", callback_data="send_command"))

    return keyboard

@dp.callback_query_handler(lambda c: c.data == 'Get_ID')
async def get_user_tgID(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(
        user_id, f"Ваш ID: {user_id}. Отправь его администратору сервера, с просьбой о выдаче доступа.",     
    )
    # Снова отправляем клавиатуру
    keyboard = await get_main_keyboard(user_id)
    await bot.send_message(
        user_id, "Выберите действие:", reply_markup=keyboard
    )

    await callback_query.answer()

@dp.message_handler(commands=['giveLevel'])
async def give_level(message: types.Message):
    args = message.text.split()
    if len(args) != 3:
        await message.reply("Использование: /giveLevel {ID} {уровень (1-4)}")
        return
    
    try:
        user_id = int(args[1])
        level = int(args[2])
        if level not in range(1, 5):
            raise ValueError
    except ValueError:
        await message.reply("Ошибка: уровень должен быть числом от 1 до 4.")
        return
    
    # Обновление уровня в базе данных
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('UPDATE users SET level = ? WHERE user_id = ?', (level, user_id))
        await db.commit()
    
    await message.reply(f"Пользователю {user_id} установлен уровень доступа {level}.")


# Состояния
class UserState(StatesGroup):
    command_input = State()  # Состояние для ввода команд


# Клавиатура с кнопкой "Назад"
back_keyboard = InlineKeyboardMarkup()
back_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))


# Функция для проверки статуса сервера
def is_server_running():
    for proc in psutil.process_iter(attrs=["name", "cmdline", "cwd"]):
        if proc.info.get("name") and proc.info.get("cmdline") and proc.info.get("cwd"):
            if ("start.bat" in proc.info["cmdline"] or "java" in proc.info["name"].lower()) and proc.info["cwd"] == SERVER_FOLDER:
                return True
    return False


# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    keyboard = await get_main_keyboard(user_id)

    await bot.send_message(
        message.chat.id,
        """Привет! Я бот для удалённого управления сервером Minecraft!
Через меня, ты можешь запускать и останавливать свой сервер в Minecraft, а также вводить команды в консоль и смотреть онлайн сервера!
Что бы продолжить, выбери один из предложенных вариантов кнопок
Если у тебя из кнопок только "Узнать свой ID", то тебе нужно обратиться к администратору сервера, скинуть ему свой ID и попросить доступ к управлению сервером.""",
        reply_markup=keyboard
    )

    # Перенос ID и UserName, используемые телеграмом, в переменные для python
    user_id = message.from_user.id
    username = message.from_user.username

    # Создание таблицы перед использованием базы
    await NewTable()

    # Вызов базы данных
    async with aiosqlite.connect('bot_database.db') as db:
        # Сохранение данных пользователя в базу
        await db.execute('''
            INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
        ''', (user_id, username))
        # Подтверждение изменений
        await db.commit()


# Обработка кнопки "Запустить сервер"
@dp.callback_query_handler(lambda c: c.data == 'start_server')
async def start_server(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_level = await get_user_level(user_id)

    if user_level < 2:
        await bot.answer_callback_query(callback_query.id, "У вас недостаточно прав для запуска сервера.", show_alert=True)
        return

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Готово, проверяйте!",
        reply_markup=await get_main_keyboard(user_id)
    )
    subprocess.Popen([SERVER_BAT_PATH], creationflags=subprocess.CREATE_NEW_CONSOLE)


# Обработка кнопки "Остановить сервер"
@dp.callback_query_handler(lambda c: c.data == 'stop_server')
async def stop_server(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_level = await get_user_level(user_id)

    if user_level < 3:
        await bot.answer_callback_query(callback_query.id, "У вас недостаточно прав для остановки сервера.", show_alert=True)
        return

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Сервер останавливается...",
        reply_markup=await get_main_keyboard(user_id)
    )
    os.system("taskkill /f /im java.exe")


# Обработка кнопки "Ввести команду в консоль"
@dp.callback_query_handler(lambda c: c.data == 'send_command')
async def send_command_prompt(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_level = await get_user_level(user_id)

    if user_level < 4:
        await bot.answer_callback_query(callback_query.id, "У вас недостаточно прав для ввода команд в консоль.", show_alert=True)
        return

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.message.chat.id,
        "Введите команду для консоли сервера:",
        reply_markup=back_keyboard
    )
    await UserState.command_input.set()


# Обработка сообщений в состоянии command_input
@dp.message_handler(state=UserState.command_input)
async def handle_console_command(message: types.Message, state: FSMContext):
    command = message.text
    try:
        with MCRcon("127.0.0.1", "1488", port=25575) as mcr:
            response = mcr.command(command)
            await message.reply(
                f"Команда '{command}' выполнена. Ответ сервера: {response}",
                reply_markup=back_keyboard
            )
    except Exception as e:
        await message.reply(
            f"Ошибка при выполнении команды: {str(e)}",
            reply_markup=back_keyboard
        )


# Обработка кнопки "Назад"
@dp.callback_query_handler(lambda c: c.data == 'back_to_main', state="*")
async def back_to_main(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    keyboard = await get_main_keyboard(user_id)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.message.chat.id,
        "Возвращаемся в главное меню:",
        reply_markup=keyboard
    )
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
