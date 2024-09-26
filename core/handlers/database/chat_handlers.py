from aiogram import F
from aiogram.types import Message

from core import bot
from core.config.settings import DB_NAME
from core.database_backend.key_phrases_db import KeyPhrasesDB
from core.handlers.database_handlers import router


@router.message(F.new_chat_member)
async def add_chat_to_db(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_init()
            await db.chat_add(message.chat.id, message.chat.full_name)


@router.message(F.left_chat_member)
async def remove_chat_from_db(message: Message) -> None:
    if message.left_chat_member.id == bot.id:
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_init()
            await db.chat_remove(message.chat.id)
