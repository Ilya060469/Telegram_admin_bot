from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b2 = KeyboardButton('/ты кто')
b3 = KeyboardButton('/меню')
b4 = KeyboardButton('Поделиться контактом', request_contact=True)
b5 = KeyboardButton('Поделиться местоположением', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b2).add(b3).row(b4, b5)
