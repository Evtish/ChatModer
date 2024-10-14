from aiogram import F, Router
from aiogram.types import Message

from core import bot
from core.handlers.basic_handlers import handle_start
from system.settings import DB_NAME
from database_backend.key_phrases_db import KeyPhrasesDB

router = Router(name=__name__)


@router.message(F.new_chat_member)
async def add_chat_to_db(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_init()
            await db.chat_add(message.chat.id, message.chat.full_name)
            await handle_start(message)


@router.message(F.left_chat_member)
async def remove_chat_from_db(message: Message) -> None:
    if message.left_chat_member.id == bot.id:
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_init()
            await db.chat_remove(message.chat.id)
