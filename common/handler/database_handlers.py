from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from .. import bot
from ..config.settings import KeyPhrasesStates, DB_NAME
from ..key_phrases_db import KeyPhrasesDB

router = Router(name=__name__)


@router.message(F.new_chat_member)
async def add_chat_to_db(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_add(message.chat.id, message.chat.full_name)


@router.message(F.left_chat_member)
async def remove_chat_from_db(message: Message) -> None:
    if message.left_chat_member.id == bot.id:
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.chat_remove(message.chat.id)


@router.message(Command('banwords'))
async def handle_key_phrases_request(message: Message, state: FSMContext) -> None:
    if message.from_user in map(lambda member: member.user, await bot.get_chat_administrators(message.chat.id)):
        await state.set_state(KeyPhrasesStates.WAIT_FOR_KEY_PHRASES)
        await message.reply('Please, send list of key phrases separated by new line')
    else:
        await message.reply('This command is for admins only')


@router.message(KeyPhrasesStates.WAIT_FOR_KEY_PHRASES)
async def set_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        new_key_phrases = message.text.split('\n')
        async with KeyPhrasesDB(DB_NAME) as db:
            for phrase in new_key_phrases:
                await db.key_phrase_add(message.chat.id, phrase)
            all_key_phrases = await db.key_phrases_get(message.chat.id)

        await state.clear()
        await message.reply(f'Key phrases have been set\n\n{markdown.hitalic('Current list:\n')}'
                            f'{'\n'.join(all_key_phrases)}')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')
