import asyncio

import logging

from aiogram import Dispatcher

from common import bot
from common.handlers import main_router

# cur_session = aiogram.client.session.aiohttp.AiohttpSession(proxy='http://proxy.server:3128')
dispatcher = Dispatcher()
dispatcher.include_router(main_router)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot was stopped')
