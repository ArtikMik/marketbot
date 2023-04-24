import sqlite3 as sq
from start_bot import bot


db = sq.connect('tgdb.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "user_id INTEGER,"
                "user_name TEXT,"
                "cart_if TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "model TEXT,"
                "price INTEGER,"
                "photo_it TEXT,"
                "brang TEXT)")
    db.commit()


def db_table_val(user_id: int, user_name: str):
    cur.execute('INSERT INTO accounts (user_id, user_name) VALUES (?, ?)',
                   (user_id, user_name))
    db.commit()


def db_table_items(model: str, price: int, brang: str, photo_it: str):
    cur.execute('INSERT INTO items (model, price, brang, photo_it) VALUES (?, ?, ?, ?)',
                   (model, price, brang, photo_it))
    db.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM items').fetchall():
        await bot.send_photo(message.chat.id, ret[3], f"Модель: {ret[1]}\nЦена: {ret[2]}\nБренд {ret[4]}")

async def sql_read2():
    return cur.execute('SELECT * FROM items').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM items WHERE model == ?', (data,))
    db.commit()


async def sql_model(item_model):
    cur.execute("SELECT model, price, brang, photo_it FROM items WHERE model = ?",
                                   (item_model,))
    db.commit()












