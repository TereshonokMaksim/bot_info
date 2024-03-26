import aiogram
import asyncio
import modules.handler_collect as handler

# Введите сюда апи ключ к своему боту
API_KEY = "6354577537:AAE92wOYz7o1VxA3r6f8ZoYmNnvy2nSlQsk"

bot = aiogram.Bot(token = API_KEY)
dp = aiogram.Dispatcher()

handler.launcher(dp = dp, bot = bot)
handler.launch_callbacks(dp = dp, bot = bot)

async def run():
    await dp.start_polling(bot)

asyncio.run(run())