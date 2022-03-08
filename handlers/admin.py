from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from creat_bot import bot
from data_base import db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import time


ID = None
ID_1 = 1161684213

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

async def make_change(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Хозяин я ваш', reply_markup=admin_kb.button_admin)
    await message.delete()

async def mute(message: types.message):
    global ID_1
    if message.from_user.id == ID_1:
        if not message.reply_to_message:
            await message.reply("это должно быть ответ на сообщение")
        await message.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=time()+600)
        await message.answer(str(message.reply_to_message.from_user.username)+"Замучен | С парвилами ознокомтесь в закрепе")
    else:
        await message.answer("У вас недостаточно прав")


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')
        print('Начат процеес добавления нового товара')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ok')
        print('Создание товара отменено')

async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название товара')

async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь описание товара')

async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену(цифрами)')

async def load_price(message: types.Message, state: FSMContext):
    global new
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await db.sql_add_command(state)
        await state.finish()
        await message.answer('товар добавлен успешно')
        print('Товар был создан и добавлен')

async def dell_callback(callback_query: types.CallbackQuery):
    await db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} удалена.', show_alert=True)

async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Описание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='товар👆', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(mute, commands=["мут"], commands_prefix="!")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(make_change, commands=['moder'], is_chat_admin=True)
    dp.register_callback_query_handler(dell_callback, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='удалить')
