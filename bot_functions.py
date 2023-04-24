import aiogram
import keyboards
from aiogram import types
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from keyboards import *
import sqlite3 as sq
import database as db
import aiohttp
from database import sql_read
from start_bot import *




class Form(StatesGroup):
    photo = State()
    brend = State()
    model = State()
    price = State()


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    db.db_table_val(user_id=us_id, user_name=us_name)
    await bot.send_message(message.chat.id, "Добрый день!\nВ этом боте вы можете заказать кроссовки разных брендов и выбрать нужные вам модели\nЧтобы выбрать модель кросовок нажмите на кнопки снизу ↓\nЧтобы связаться с ", reply_markup=start)
    if message.from_user.id == int(ADMIN_ID):
        await bot.send_message(message.chat.id, "Привет админ)", reply_markup=main_admin)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю")


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'shoes')
async def choose_brand(callback_query: types.CallbackQuery):
    items = [row[0] for row in db.cur.execute('SELECT brang FROM items').fetchall()]
    markup = InlineKeyboardMarkup(row_width=1)
    for brang in items:
        markup.add(InlineKeyboardButton(text=brang, callback_data=f"brand_{brang}"))
    await bot.send_message(callback_query.from_user.id, "Выберите бренд", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('brand_'))
async def choose_model(callback_query: types.CallbackQuery):
    brang = callback_query.data.split('_')[1]
    items = [row[0] for row in db.cur.execute('SELECT model FROM items WHERE brang = ?', (brang,)).fetchall()]
    markup = InlineKeyboardMarkup(row_width=1)
    for model in items:
        markup.add(InlineKeyboardButton(text=model, callback_data=f"model_{model}"))
    await bot.send_message(callback_query.from_user.id, f"Выберите модель бренда {brang}", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith('model_'))
async def show_item(callback_query: types.CallbackQuery):
    model = callback_query.data.split('_')[1]
    # получение данных из таблицы
    db.cur.execute("SELECT model, price, brang, photo_it FROM items WHERE model = ?",
                               (model,))
    data = db.cur.fetchall()
    # форматирование данных в виде строки
    text = ''
    for row in data:
        text += f"model: {row[0]}\nprice: {row[1]}$\nbrend: {row[2]}"
        await bot.send_message(callback_query.from_user.id, text=text)
        await bot.send_photo(callback_query.from_user.id, photo=row[3])
        await bot.send_message(callback_query.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'Заказать {row[0]}', callback_data=f"order_{row[0]}")))


@dp.callback_query_handler(lambda c: c.data.startswith('order_'))
async def show_item(callback_query: types.CallbackQuery):
    model = callback_query.data.split('_')[1]
    # получение данных из таблицы
    db.cur.execute("SELECT model, price, brang, photo_it FROM items WHERE model = ?",
                               (model,))
    data = db.cur.fetchall()
    # форматирование данных в виде строки
    text = ''
    for row in data:
        text += f"спасибо за заказ!\nВаш заказ:\nБренд: {row[2]}\nМодель {row[0]}\nЦена заказа составит {row[1]}$"
        await bot.send_message(callback_query.from_user.id, text=text)
        await bot.send_photo(callback_query.from_user.id, photo=row[3])
        await bot.send_message(chat_id=ADMIN_ID, text=f"Поступил заказ")




@dp.message_handler(text='Удалить товар')
async def delete_items(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        read = await db.sql_read2()
        for ret in read:
            await bot.send_photo(message.chat.id, ret[3], f"Модель: {ret[1]}\nЦена: {ret[2]}\nБренд {ret[4]}")
            await bot.send_message(message.chat.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f"del {ret[1]}")))


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await bot.send_message(message.chat.id, f"Покупать для более подробной информации писать сюда: https://t.me/artemmikhniuk")


@dp.message_handler(text='Весь каталог')
async def contacts(message: types.Message):
    await db.sql_read(message)


@dp.message_handler(text='Админ-панель')
async def panel(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await bot.send_message(message.chat.id, "Вы вошли в админ-панель", reply_markup=admin_panel)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю")


@dp.message_handler(text='Назад')
async def panel(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await bot.send_message(message.chat.id, "Вы вернулись назад", reply_markup=main_admin)
    else:
        await bot.send_message(message.chat.id, "Я тебя не понимаю")


@dp.message_handler(text='Добавить товар')
async def update_tovar(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        await bot.send_message(message.chat.id, "Добавитте товар\nНапишите бренд:")
        await Form.brend.set()
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю")


@dp.message_handler(state=Form.brend)
async def process_model(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['brend'] = message.text
        await message.reply("Введите название модели: ")
        await Form.model.set()


@dp.message_handler(state=Form.model)
async def process_user_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
    await message.answer("Теперь введите цену: ")
    await Form.price.set()  # либо же UserState.adress.set()


@dp.message_handler(state=Form.price)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await message.reply("Теперь отправте фото модели: ")
    await Form.photo.set()


@dp.message_handler(state=Form.photo, content_types=types.ContentType.PHOTO)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        photo_item = data['photo'] = message.photo[-1].file_id
    send_shoes = f"brend: {data['brend']}\n" \
    f"model: {data['model']}\n" \
    f"price: {data['price']}$"
    brend_item  = f"{data['brend']}"
    model_item = f"{data['model']}"
    price_item = f"{data['price']}"
    await bot.send_message(message.chat.id, send_shoes)
    await bot.send_photo(message.chat.id, photo=photo_item)
    db.db_table_items(brang=brend_item, price=price_item, model=model_item, photo_it=photo_item)
    await state.finish()


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await bot.send_message(message.chat.id, "Каталог товаров)", reply_markup=catalog_list)


@dp.message_handler()
async def answer(message: types.Message):
    await bot.send_message(message.chat.id, 'Я тебя не понимаю')



async def main():
    executor.start_polling(dp, on_startup=on_startup)