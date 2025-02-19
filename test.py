import logging
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# Твой токен от BotFather
TOKEN = "8100350669:AAE_GPbA0QyTd95YkfUccFaJ1lEi0GcTtcY"

# Создаём объект бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Функция для парсинга данных
def get_enrollment_data():
    url = "https://lk.msu.ru/course/view?id=3794"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем нужный <p>
        target_p = None
        for p in soup.find_all('p'):
            strong = p.find('strong')
            if strong and "Записалось / всего мест" in strong.text:
                target_p = p
                break

        if target_p:
            br = target_p.find('br')
            if br and br.next_sibling:
                enrolled_count = br.next_sibling.strip()
                enrolled, total = map(str.strip, enrolled_count.split('/'))
                return f"Записалось: {enrolled} из {total} мест."
        return "Данные не найдены."
    return f"Ошибка при получении данных: {response.status_code}"

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Отправь /check, чтобы узнать число записавшихся.")

# Обработчик команды /check
@dp.message(Command("check"))
async def check_command(message: Message):
    data = get_enrollment_data()
    await message.answer(data)

# Функция запуска бота
async def main():
    await dp.start_polling(bot)

# Запускаем бота
if __name__ == "__main__":
    asyncio.run(main())

