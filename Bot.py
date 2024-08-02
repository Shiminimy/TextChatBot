import logging
import aiogram
import asyncio
import json
#-----------------------------------------------------------------------------------------------------------------------------------------
from handlers import register_handlers
from keyboards import start_keyboard
from aiogram.utils import executor
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from func import handlers
#-----------------------------------------------------------------------------------------------------------------------------------------
dp = Dispatcher()
#-----------------------------------------------------------------------------------------------------------------------------------------
from config_reader import config
#-----------------------------------------------------------------------------------------------------------------------------------------
def load_data():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

class LoginState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

class RegisterState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

register_handlers(dp, load_data, save_data, LoginState, RegisterState, start_keyboard)
#-----------------------------------------------------------------------------------------------------------------------------------------
handlers.reg_handler(dp)
bot = Bot(token=config.bot_token.get_secret_value())
#-----------------------------------------------------------------------------------------------------------------------------------------
async def main():
    await dp.start_polling(bot)
#-----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Stopped")   