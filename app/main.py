from config import *

import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router


dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started")
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stoped")


