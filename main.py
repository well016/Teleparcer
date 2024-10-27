import logging
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = '7723642778:AAFyox7V__q5S6iYmbD8faOZmjjG85ru8kU'

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаем объект бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# URL для авторизации и парсинга данных
login_url = 'https://shelly.kpfu.ru/e-ksu/private_office.kfuscript'
data_url = 'https://shelly.kpfu.ru/e-ksu/private_office_data'

# Ваши учетные данные
payload = {
    'p_login': 'RailRSabirov',
    'p_pass': 'QMT0Qk5mm7'
}


def parse_data():
    with requests.Session() as session:
        # Выполняем логин
        response = session.post(login_url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if response.status_code == 200:
            # Используем сессию для доступа к данным
            response = session.get(data_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Парсим нужные данные (пример: находим элемент с необходимыми данными)
            data_element = soup.find('div', class_='top_block')
            return data_element.text if data_element else 'Не удалось найти данные.'
        else:
            return 'Ошибка логина'


# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Используйте /getdata, чтобы получить данные.")


# Обработчик команды /getdata
@dp.message(Command(commands=['getdata']))
async def get_data(message: types.Message):
    await message.reply("Пожалуйста, подождите, идет обработка запроса...")
    data = parse_data()
    await message.reply(f'Ваши данные: {data}')


# Запуск бота
if __name__ == '__main__':
    import asyncio


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
