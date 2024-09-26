from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from .database import check_user_is_admin
from .. import bot
from ..config.settings import KeyPhrasesStates, DB_NAME
from core.database_backend.key_phrases_db import KeyPhrasesDB

router = Router(name=__name__)


@router.message(Command('check_banwords'))
async def check_key_phrases(message: Message) -> None:
    if message.from_user in map(lambda member: member.user, await bot.get_chat_administrators(message.chat.id)):
        async with KeyPhrasesDB(DB_NAME) as db:
            cur_chat_key_phrases = await db.key_phrases_get(message.chat.id)
        await message.reply(f'{markdown.hitalic('Current list:\n')}{'\n'.join(cur_chat_key_phrases)}')
    else:
        await message.reply('This command is for admins only')


@router.message(Command('add_banwords'))
@check_user_is_admin
async def handle_add_key_phrases_request(message: Message, state: FSMContext) -> None:
    await state.set_state(KeyPhrasesStates.ADD_KEY_PHRASES)
    await message.reply('Please, send list of key phrases separated by new line')


@router.message(KeyPhrasesStates.ADD_KEY_PHRASES)
async def add_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        new_key_phrases = message.text.split('\n')
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.key_phrase_init()
            for phrase in new_key_phrases:
                await db.key_phrase_add(message.chat.id, phrase)
            all_key_phrases = await db.key_phrases_get(message.chat.id)

        await state.clear()
        await message.reply(f'Key phrases have been set\n\n{markdown.hitalic('Current list:\n')}'
                            f'{'\n'.join(all_key_phrases)}')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')


@router.message(Command('remove_banwords'))
@check_user_is_admin
async def handle_remove_key_phrases_request(message: Message, state: FSMContext) -> None:
    await state.set_state(KeyPhrasesStates.REMOVE_KEY_PHRASES)
    await message.reply('Please, send list of key phrases separated by new line')


@router.message(KeyPhrasesStates.REMOVE_KEY_PHRASES)
async def add_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        new_key_phrases = message.text.split('\n')
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.key_phrase_init()
            for phrase in new_key_phrases:
                await db.key_phrase_add(message.chat.id, phrase)
            all_key_phrases = await db.key_phrases_get(message.chat.id)

        await state.clear()
        await message.reply(f'Key phrases have been set\n\n{markdown.hitalic('Current list:\n')}'
                            f'{'\n'.join(all_key_phrases)}')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')
