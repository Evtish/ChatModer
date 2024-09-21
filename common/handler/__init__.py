from aiogram import Router

from .basic_handlers import router as base_router
from .admin_handlers import router as admin_router
from .database_handlers import router as database_router
from .keywords_handlers import router as keywords_router

main_router = Router(name=__name__)
main_router.include_routers(base_router, admin_router, database_router)

main_router.include_router(keywords_router)  # must be the latest

# __all__ = ('main_router')
