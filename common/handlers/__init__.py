# __all__ = {'main_router'}

from aiogram import Router

from .base import router as base_router
from .admin import router as admin_router
from .keywords import router as keywords_router

main_router = Router(name=__name__)
main_router.include_routers(base_router, admin_router)

main_router.include_router(keywords_router)  # must be the latest
