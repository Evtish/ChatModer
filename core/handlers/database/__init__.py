from functools import wraps
from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core import bot


def check_user_is_admin(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext) -> None:
        if message.from_user in map(lambda member: member.user, await bot.get_chat_administrators(message.chat.id)):
            func(message, state)
        else:
            await message.reply('This command is for admins only')

    return wrapper
