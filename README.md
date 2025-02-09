# 🚀 Telegram Bot for Minecraft Server Management

Этот бот позволяет удобно управлять сервером Minecraft через Telegram, предоставляя интуитивно понятный интерфейс для запуска, остановки и администрирования сервера.

---

## 🎮 Возможности
✅ Получение Telegram ID пользователя  
✅ Гибкая система уровней доступа  
✅ Запуск и остановка сервера Minecraft  
✅ Выполнение команд в консоли сервера  

---

## 📌 Установка

### 🔧 Требования
- Python 3.8+
- Telegram Bot API Token
- Установленные зависимости из `requirements.txt`

### 📥 Установка зависимостей
```bash
pip install -r requirements.txt
```

---

## ⚙️ Конфигурация
Перед запуском замените `API_TOKEN` в `bot.py` на ваш API-ключ от Telegram Bot API.

---

## ▶️ Запуск бота
```bash
python bot.py
```

---

## 🛠 Использование
После запуска бота в Telegram доступны команды:
- `/start` – Начало работы с ботом и отображение главного меню.
- `/giveLevel {ID} {уровень}` – Выдача уровня доступа пользователю (1-4).

### 🔑 Уровни доступа
- **1️⃣ Базовый** – Только просмотр ID.
- **2️⃣ Оператор** – Запуск сервера.
- **3️⃣ Администратор** – Остановка сервера.
- **4️⃣ Суперадмин** – Полный доступ, включая выполнение команд в консоли.

---

## 🗄 База данных
Бот использует `aiosqlite` для хранения информации о пользователях и их уровне доступа.

---

## 🔌 Управление сервером
- 📊 Использует `psutil` для мониторинга статуса сервера.
- ▶️ Запуск сервера осуществляется через `start.bat`.
- ⏹ Остановка сервера выполняется завершением процесса `java.exe`.
- 💻 Команды в консоли сервера выполняются через `MCRcon`.

---

## 👨‍💻 Разработчик
**Автор:** [Ваше имя или никнейм]  
✉️ Связь: [Ваш контакт или ссылка]

---

## 📜 Лицензия
Этот проект распространяется под лицензией **MIT**.

