from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

avtorizachia = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Вход', callback_data='login'),
         InlineKeyboardButton(text='Регистрация', callback_data='register')
    ]
])