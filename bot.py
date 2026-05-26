import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = "YOUR_BOT_TOKEN"
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello!Send me a Pokemon name you want to see!")

@dp.message()
async def send_pokemon_info(message: Message):
    pokemon_name = message.text.lower().strip()  # type: ignore
    await message.answer("I'm looking for your Pokemon!")

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    name = data["name"].capitalize()
                    image_url = data["sprites"]["front_default"]
                    pokemon_type = data["types"][0]["type"]["name"]
                    caption_text = f"👾 Pokemon: {name}\n⚡ Тип: {pokemon_type}"
                    if image_url:
                        await message.answer_photo(photo = image_url, caption = caption_text)
                    else:
                        await message.answer(caption_text)
                elif response.status == 404:
                    await message.answer("Enter a name in English! Don't use numbers and symbols!")
                else:
                    await message.answer(f"Error! Error's code is {response.status}")
        except Exception as e:
            await message.answer("Something went wrong! Try again later!")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
