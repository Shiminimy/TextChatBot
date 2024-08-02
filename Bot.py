import logging
import aiogram
import asyncio
from aiogram import Dispatcher, Bot

from aiogram.filters import CommandStart
from aiogram.types import Message
from func import handlers
dp = Dispatcher()

from config_reader import config


handlers.reg_handler(dp)
bot = Bot(token=config.bot_token.get_secret_value())






async def main():
    await dp.start_polling(bot)
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Stopped")   