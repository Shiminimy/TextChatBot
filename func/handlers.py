from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.dispatcher import router
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods import EditMessageText
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
dp = Dispatcher()
router = Router()
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
from aiogram.types import Message
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
#-----------------------------------------------------------------------------------------------------------------------------------------
async def start(message: Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=start_keyboard())
#-----------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data in ['login', 'register'])
async def process_callback(callback_query: types.CallbackQuery):
    action = callback_query.data
    if action == 'login':
        await dp.bot.send_message(callback_query.from_user.id, 'Введите ваш логин:')
        await LoginState.waiting_for_username.set()
    elif action == 'register':
        await dp.bot.send_message(callback_query.from_user.id, 'Введите ваш логин для регистрации:')
        await RegisterState.waiting_for_username.set()
    @dp.message_handler(state=LoginState.waiting_for_username)
    async def process_login_username(message: types.Message, state: FSMContext):
        username = message.text
        data = load_data()
        if username in data and data[username]['attempts'] < 7:
            await message.answer('Введите ваш пароль:')
            await LoginState.waiting_for_password.set()
            await state.update_data(username=username)
        elif username in data:
            await message.answer('Превышен лимит попыток. Попробуйте позже.')
        else:
            await message.answer('Пользователь не найден. Попробуйте еще раз.')
            data[username] = data.get(username, {'attempts': 0})
            data[username]['attempts'] += 1
            save_data(data)
#-----------------------------------------------------------------------------------------------------------------------------------------
    @dp.message_handler(state=LoginState.waiting_for_password)
    async def process_login_password(message: types.Message, state: FSMContext):
        password = message.text
        state_data = await state.get_data()
        username = state_data.get('username')
        data = load_data()
        if data.get(username, {}).get('password') == password:
            await message.answer('Вы вошли успешно!')
            data[username]['attempts'] = 0
            save_data(data)
        else:
            await message.answer('Неверный пароль. Попробуйте снова.')
            data[username]['attempts'] += 1
            save_data(data)
        
        if data[username]['attempts'] >= 7:
            await message.answer('Превышен лимит попыток. Попробуйте позже.')
        await state.finish()
#-----------------------------------------------------------------------------------------------------------------------------------------
    @dp.message_handler(state=RegisterState.waiting_for_username)
    async def process_register_username(message: types.Message, state: FSMContext):
        username = message.text
        data = load_data()
        if username in data:
            await message.answer('Этот логин уже занят. Попробуйте другой.')
        else:
            await message.answer('Введите ваш пароль для регистрации:')
            await RegisterState.waiting_for_password.set()
            await state.update_data(username=username)
#-----------------------------------------------------------------------------------------------------------------------------------------
    @dp.message_handler(state=RegisterState.waiting_for_password)
    async def process_register_password(message: types.Message, state: FSMContext):
        password = message.text
        state_data = await state.get_data()
        username = state_data.get('username')
        data = load_data()
        data[username] = {'password': password, 'attempts': 0}
        save_data(data)
        await message.answer('Вы зарегистрированы успешно!')
        await state.finish()
#-----------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['ai'])
async def echo(message: types.Message):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as f:
        intents = json.load(f)

    bot_name = "T"
    FILE = "data.pth"

    data = torch.load(FILE, weights_only=True)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)

    model.load_state_dict(model_state)
    model.eval()
    
    sentence = message.text
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).float().to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]


    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:

        for intent in intents["intents"]:
            if tag == intent["tag"]:
                await message.answer(f'{bot_name}: {random.choice(intent["responses"])}')
    else:
        #реализация отправки стика думаю будет прикольно такое реализовать, проверим как работает после всего
        #sticker_id = 'CAACAgIAAxkBAAEMmYpmrqds1mQgWTdK4Sn5rJDZWV4AAYYAAs5SAAJRaEhJsTkW5jcTYaE1BA'
        #await bot.send_sticker(chat_id=message.chat.id, sticker=sticker_id)
        await message.answer(f'{bot_name}: Не понимаю..............')

#-----------------------------------------------------------------------------------------------------------------------------------------
def reg_handler(dp):
    dp.message.register(start, Command("start"))
    dp.message.register(echo)
