from aiogram import Router

from .chat_handlers import router as chat_router
# from .detected_message_handlers import router as detected_message_router
from .key_phrase_handlers import router as key_phrase_router

router = Router(name=__name__)
router.include_routers(chat_router, key_phrase_router)

__all__ = 'router'