import asyncio
import logging
from bot.handlers.user import router
from bot.handlers.admin import admin
from aiogram import Bot, Dispatcher
from bot.config import TOKEN
from bot.db.database import init_db


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)
dp.include_router(admin)

async def on_startup(dispatcher: Dispatcher):
    await init_db()

async def main():
    await on_startup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
