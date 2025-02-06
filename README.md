# BOT1k - Telegram Minecraft Server Manager

## @ThalyaevBot

BOT1k предназначен для удалённого запуска серверов Minecraft через Telegram.

## 🔧 Логика работы:
- Один компьютер выступает в роли **хоста** сервера Minecraft со стартовым файлом `start.bat`.
- Бот позволяет **удалённо запускать** этот файл по команде в Telegram, независимо от местоположения пользователя.
- Любой желающий может **скачать и настроить** бота для работы со своим сервером.
- **Хост сервера** может предоставлять доступ к управлению другими пользователям Telegram.
- Бот поддерживает лишь **один** сервер, для добавления ещё одного сервера, для него придётся создать ещё одного чат-бота.
- БОт даёт предоставляет к **удалённому** доступу к консоли сервера, для ввода внутриигровых команд на вашем сервере.

---

# 🚀 ОБНОВЛЕНИЯ

### 🎉 31.01.2025 12:58
✅ База данных стала **асинхронной** благодаря `aioSQLite`.
✅ Добавлено **виртуальное окружение** с `Python 3.11` и необходимыми библиотеками.
✅ Добавлен стартовый файл `start.bat` для запуска работы бота.

### 🎉 02.02.2025 20:57
✅ Бот теперь **реагирует на кнопку запуска сервера**, автоматически запуская нужный файл.

### 🎉 03.02.2025 15:56
✅ Добавлена **система проверки доступа** к серверу для каждого пользователя.
✅ Разработана **система выдачи прав** пользователям через команды в чате с ботом.

---

# 📥 УСТАНОВКА БОТА

### 1️⃣ Клонирование репозитория
```bash
git clone https://github.com/your-repo/BOT1k.git
cd BOT1k
```

### 2️⃣ Создание виртуального окружения и установка зависимостей
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

### 3️⃣ Настройка бота
1. Создайте бота через [BotFather](https://t.me/BotFather) и получите API токен.
2. В файле `bot.py` замените `YOUR_TELEGRAM_BOT_TOKEN` на ваш API токен.
3. Укажите путь к `start.bat` вашего сервера Minecraft.

### 4️⃣ Запуск бота
```bash
python bot.py
```

Бот готов к работе! Теперь вы можете управлять вашим сервером Minecraft через Telegram.

---

## 📌 Как использовать?
1. Настроить бота на хосте сервера Minecraft.
2. Выдать права пользователям для запуска серверов.
3. Управлять серверами через Telegram!

📢 **Оставайтесь с нами для новых обновлений!** 🚀
