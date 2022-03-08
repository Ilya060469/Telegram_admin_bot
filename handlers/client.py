from aiogram import types, Dispatcher
from creat_bot import bot
from keyboards import kb_client
from data_base import db

async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Я тут и могу помочь', reply_markup=kb_client)
    except:
        await message.reply('напиши боту в лс \n@Botforyoutube_bot')

async def command_dialog(message: types.Message):
    await bot.send_message(message.from_user.id, 'Я бот пиццерии\n'
                                                 'чем могу тем помогу\n'
                                                 'нашел ошибку пиши - @LoliLord1')

async def menu(message: types.Message):
    await db.read_sql_db(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_dialog, commands=['ты кто'])
    dp.register_message_handler(menu, commands=['меню'])
