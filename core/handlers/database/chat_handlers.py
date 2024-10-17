from aiogram import F, Router
from aiogram.types import Message

from core import bot
from core.handlers.basic_handlers import handle_start
from database_backend.engine import insert_row
from database_backend.models import Chat
from system.settings import DB_NAME
from database_backend.key_phrases_db import KeyPhrasesDB

router = Router(name=__name__)


@router.message(F.new_chat_member)
async def add_chat_to_db(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        await handle_start(message)
        await insert_row(Chat, chat_id=message.chat.id, chat_fullname=message.chat.full_name)
        # async with KeyPhrasesDB(DB_NAME) as db:
        #     await db.chat_init()
        #     await db.chat_add(message.chat.id, message.chat.full_name)


@router.message(F.left_chat_member)
async def remove_chat_from_db(message: Message) -> None:
    if message.left_chat_member.id == bot.id:
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_init()
            await db.chat_remove(message.chat.id)
