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






async def start(message: Message):
    await message.answer("Привет напиши мне что нибудь из этого или похожее на это: patterns: Привет Как дела Есть кто-нибудь? Привет Добрый день Пока, До встречи, До свидания, Увидимся позже Спасибо, Это полезно, Большое спасибо!, Какие предметы у вас есть?, Какие виды товаров у вас есть?, Что вы продаете? Принимаете ли вы кредитные карты? Принимаете ли вы Mastercard? Могу ли я заплатить с помощью Paypal? Только наличные? Сколько времени занимает доставка? Сколько времени потребуется на доставку?Когда я получу свою посылку? Расскажи мне анекдот! Расскажи мне что-нибудь смешное! Знаешь ли ты анекдот?")




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
        await message.answer(f'{bot_name}: Не понимаю..............')











def reg_handler(dp):
    dp.message.register(start, Command("start"))
    dp.message.register(echo)