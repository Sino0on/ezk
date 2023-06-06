import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = ''

keyboard = [
    [types.KeyboardButton(text='❓Вопросы❓')],
    [types.KeyboardButton(text='О нас')],
    [types.KeyboardButton(text='Контакты')],
]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    kb = types.ReplyKeyboardMarkup(keyboard=keyboard)
    await message.reply("Добрый день\nЯ телеграмм бот который поможет и ответит на ваши вопросы", reply_markup=kb)


@dp.message_handler()
async def echo(message: types.Message):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    if message.text == '❓Вопросы❓':
        for i in data['quistions'].keys():
            inline_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))

        await message.answer('Вот ответы на твои вопросы', reply_markup=inline_keyboard)
    elif message.text == 'О нас':
        await message.answer(data['About'])
    elif message.text == 'Контакты':
        await message.answer(data['Контакты'])


@dp.callback_query_handler()
async def call_back(call: types.CallbackQuery):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    await bot.send_message(chat_id=call.from_user.id, text=data['quistions'][call.data])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
