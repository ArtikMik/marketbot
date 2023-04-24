from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import database as db


start = ReplyKeyboardMarkup(resize_keyboard=True)
start.add('Каталог').add('Контакты').add('Весь каталог')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Контакты').add('Админ-панель').add('Весь каталог')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add("Назад")

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Кроссовки', callback_data='shoes'))


nike = InlineKeyboardButton('Nike', callback_data='nike')
adidas = InlineKeyboardButton('Adidas', callback_data='adidas')
puma = InlineKeyboardButton('Puma', callback_data='puma')

full_shoes = InlineKeyboardMarkup().add(nike, adidas, puma)



