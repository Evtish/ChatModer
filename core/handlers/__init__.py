from aiogram import Router

from .basic_handlers import router as base_router
from .direct_chat_handlers import router as admin_router
from core.handlers.database import router as database_router

router = Router(name=__name__)
router.include_routers(base_router, admin_router, database_router)

__all__ = 'router'
