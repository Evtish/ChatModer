from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from system.media import ADMIN_GIF

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer('Hi!')
    # await message.answer_animation(ADMIN_GIF)


@router.message(Command('help'))
async def handle_help(message: Message) -> None:
    await message.answer('*help*')
