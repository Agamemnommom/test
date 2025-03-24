import logging
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

TOKEN = "МОЙ_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Список курсов с их URL и названиями для удобства
COURSES = [
    {"name": "Курс 1", "url": "https://lk.msu.ru/course/view?id=3794"},
    {"name": "Курс 2", "url": "https://lk.msu.ru/course/view?id=3795"},
    {"name": "Курс 3", "url": "https://lk.msu.ru/course/view?id=3793"},
    {"name": "Курс 4", "url": "https://lk.msu.ru/course/view?id=3597"},
]

def get_enrollment_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for p in soup.find_all('p'):
            strong = p.find('strong')
            if strong and "Записалось / всего мест" in strong.text:
                br = p.find('br')
                if br and br.next_sibling:
                    enrolled_count = br.next_sibling.strip()
                    enrolled, total = map(str.strip, enrolled_count.split('/'))
                    return f"Записалось: {enrolled} из {total} мест."
    return "Данные нема."

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Здарова! Отправь /check, чтобы узнать число записавшихся на прекрасные курсы МФК.")

@dp.message(Command("check"))
async def check_command(message: Message):
    for course in COURSES:
        data = get_enrollment_data(course["url"])
        await message.answer(f"{course['name']}: {data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
