from aiogram import types, Dispatcher
import json, string
from creat_bot import bot
from time import time

async def mat_delete(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()} \
            .intersection(set(json.load(open('cenz.json')))):
        await message.answer('мат и вражда запрещены')
        await message.delete()
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time()+300)
    elif message.text.lower() == 'привет':
        await message.reply('и тебе привет')
    elif message.text.lower() == 'холоп':
        if message.from_user.id == 1161684213:
            await message.reply('Слушаюсь и повинуюсь')
        else:
            await message.reply('сам холоп')
    elif message.text.lower().startswith('посоветуй'):
        if message.from_user.id == 1161684213:
            if 'пицу' in message.text.lower().split():
                await message.reply('Я советую заказать пицу с грибами')
            else:
                await message.reply('Даже не знаю что посоветовать')
    else:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                await message.delete()
                await message.answer('ссылки запрещены')
            else:
                return

async def handler_new_member(message):
    await bot.send_message(message.chat.id, "Добро пожаловать в группу пиццерии!\n"
                                            "отпиши мне @Botforyoutube_bot")

async def left_member(message):
    await bot.send_message(message.chat.id, "Будем рады вам снова")

def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(mat_delete)
    dp.register_message_handler(handler_new_member, content_types=["new_chat_members"])
    dp.register_message_handler(left_member, content_types=["left_chat_member"])
