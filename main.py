import asyncio

import logging

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext

from core import bot
from core.handlers import router as main_router
from system.settings import KeyPhrasesStates

# cur_session = aiogram.client.session.aiohttp.AiohttpSession(proxy='http://proxy.server:3128')
dispatcher = Dispatcher()
dispatcher.include_router(main_router)


async def aiogram_main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    # await FSMContext.set_state(KeyPhrasesStates.SEARCH_KEY_PHRASES)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(aiogram_main())
    except KeyboardInterrupt:
        logging.log(level=logging.INFO, msg='Bot was stopped')
