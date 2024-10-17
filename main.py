import asyncio

import logging

from aiogram import Dispatcher

from core import bot
from core.handlers import router as main_router

from database_backend.engine import sqlalchemy_main

# cur_session = aiogram.client.session.aiohttp.AiohttpSession(proxy='http://proxy.server:3128')
dispatcher = Dispatcher()
dispatcher.include_router(main_router)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await sqlalchemy_main()
    # await FSMContext.set_state(KeyPhrasesStates.SEARCH_KEY_PHRASES)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.log(level=logging.INFO, msg='Bot was stopped')
