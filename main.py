from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from parcer import Parser
import asyncio
import sqlite3
import tokken
# Подключение к базе данных SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        login TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Инициализация бота и диспетчера
bot = Bot(token=tokken.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Определение состояний
class ScheduleStates(StatesGroup):
    login = State()
    password = State()

# Обработчик команды /start
@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT login, password FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        await message.answer("Вы уже авторизованы. Можете сразу ввести день недели, чтобы получить расписание.")
    else:
        await message.answer("\U0001F916 Привет! Введите ваш логин для начала.")
        await state.set_state(ScheduleStates.login)

# Обработчик ввода логина
@router.message(ScheduleStates.login)
async def get_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите ваш пароль.")
    await state.set_state(ScheduleStates.password)

# Обработчик ввода пароля
@router.message(ScheduleStates.password)
async def get_password(message: Message, state: FSMContext):
    data = await state.get_data()
    login = data['login']
    password = message.text

    # Сохранение логина и пароля в базе данных
    user_id = message.from_user.id
    cursor.execute('REPLACE INTO users (user_id, login, password) VALUES (?, ?, ?)', (user_id, login, password))
    conn.commit()

    await message.answer("Вы успешно авторизовались! Теперь можете ввести день недели, чтобы получить расписание.")
    await state.clear()

# Обработчик выбора дня недели (без состояния)
@router.message()
async def get_schedule(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT login, password FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        await message.answer("Сначала вам нужно авторизоваться. Введите команду /start для начала.")
        return

    login, password = user_data
    day_of_week = message.text

    try:
        parser = Parser(login, password)
        schedule = parser.get_table_by_day(day_of_week)
        await message.answer(schedule)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

# Обработчик команды /cancel
@router.message(Command('cancel'))
@router.message(F.text.lower() == 'отмена')
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена.")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
