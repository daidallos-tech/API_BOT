import asyncio
import aiohttp
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN`"
dp = Dispatcher()

BASE_URL = "https://v2.jokeapi.dev/joke/"
VALID_CATEGORIES = ["Any", "Programming", "Spooky", "Dark"]
START_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Any"), KeyboardButton(text="Programming")],
        [KeyboardButton(text="Spooky"), KeyboardButton(text="Dark")]
    ],
    resize_keyboard=True
)

# Handler start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello! I know different jokes! Do you want to know one of them?",
    reply_markup = START_KEYBOARD
    )

# Sent Joke if user type any message
@dp.message()
async def send_joke(message: Message, session: aiohttp.ClientSession):
    #joke = message.text.lower().strip()  # type: ignore
    category = message.text

    if category not in VALID_CATEGORIES:
        await message.answer("Use buttons to choose valid category!")
        return
    
    await message.answer("I'm thinking of joke...")
    await asyncio.sleep(4)
    await message.answer("Oh, I got it! Listen!")
    await asyncio.sleep(1)

    url = f"{BASE_URL}{category}"

    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data["type"] == "single":
                    await message.answer(data["joke"])
                else:
                    await message.answer(data["setup"])
                    await asyncio.sleep(2)
                    await message.answer(data["delivery"])
            else:
                await message.answer(f"Error! Code: {response.status}")
    except Exception as e:
            logging.error(f"Error! Error type is {e}")
            await message.answer("Something went wrong! Try again later!")

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    async with aiohttp.ClientSession() as session:
        await dp.start_polling(bot, session=session)

if __name__ == "__main__":
    asyncio.run(main())
