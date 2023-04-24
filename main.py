from bot_functions import *
import asyncio


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)