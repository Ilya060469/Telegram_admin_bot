from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b_load = KeyboardButton('/загрузить')
b_delete = KeyboardButton('/удалить')

button_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(b_load, b_delete)
