from functools import wraps
from typing import Callable

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from system.settings import Callback, DB_NAME, KeyPhrasesStates
# from system.media import HAMSTER_COMBAT, BAD_WORDS

import core
from core import bot, MessageManager
from core.informer.get_info_messages import get_for_admins_message
from database_backend.key_phrases_db import KeyPhrasesDB

import pymorphy3

router = Router(name=__name__)
morph = pymorphy3.MorphAnalyzer()

kb_action_buttons = {
    'Ignore': Callback.IGNORE_MESSAGE,
    'Delete message': Callback.DELETE_MESSAGE,
    'Mute user': Callback.MUTE_USER,
    'Ban user': Callback.BAN_USER
}


class KeyPhraseManager(MessageManager):
    def convert_to_normal_form(self) -> str:
        normal_form_phrase = []
        try:
            for word in self.get_text_or_caption().split():
                normal_form_phrase.append(morph.parse(word.strip())[0].normal_form)
        except AttributeError:
            pass
        return ' '.join(normal_form_phrase)

    async def info_admins(self) -> None:
        try:
            for cur_admin in await core.bot.get_chat_administrators(self.message.chat.id):
                if not cur_admin.user.is_bot:
                    await core.bot.send_message(
                        cur_admin.user.id,
                        get_for_admins_message(),
                        reply_markup=core.create_inline_kb(kb_action_buttons)
                    )
                    # await core.bot.send_photo(
                    #     cur_admin.user.id,
                    #     HAMSTER_COMBAT,
                    #     caption=get_for_admins_message(),
                    #     reply_markup=core.create_inline_kb(kb_action_buttons)
                    # )
        except (AttributeError, TelegramBadRequest):
            pass

    async def detect_kw(self) -> Message:
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.key_phrase_init()
            key_phrases = await db.key_phrases_get(self.message.chat.id)
        normal_form_key_phrase = self.convert_to_normal_form()
        for kw_phrase in key_phrases:
            if kw_phrase in normal_form_key_phrase:
                return self.message


key_phrase_manager = KeyPhraseManager()


def check_user_is_admin(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> None:
        message: Message = args[0]
        if message.from_user in map(lambda member: member.user, await bot.get_chat_administrators(message.chat.id)):
            await func(*args, **kwargs)
        else:
            await message.reply('This command is for admins only')

    return wrapper


@router.message(Command('check_banwords'))
@check_user_is_admin
async def check_key_phrases(message: Message) -> None:
    async with KeyPhrasesDB(DB_NAME) as db:
        cur_chat_key_phrases = await db.key_phrases_get(message.chat.id)
    await message.reply(f'{markdown.hitalic('Current list:\n')}{'\n'.join(cur_chat_key_phrases)}')


@router.message(Command('add_banwords'))
@check_user_is_admin
async def handle_add_key_phrases_request(message: Message, state: FSMContext) -> None:
    await state.set_state(KeyPhrasesStates.ADD_KEY_PHRASES)
    await message.reply('Please, send list of key phrases separated by new line')


@router.message(KeyPhrasesStates.ADD_KEY_PHRASES)
async def add_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        if message.text.startswith('/'):
            raise AttributeError

        new_key_phrases = message.text.split('\n')
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.key_phrase_init()
            for phrase in new_key_phrases:
                await db.key_phrase_add(message.chat.id, phrase)
            all_key_phrases = await db.key_phrases_get(message.chat.id)

        await state.set_state(KeyPhrasesStates.SEARCH_KEY_PHRASES)
        await message.reply(f'Key phrases have been set\n\n{markdown.hitalic('Current list:\n')}'
                            f'{'\n'.join(all_key_phrases)}')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')


@router.message(Command('remove_banwords'))
@check_user_is_admin
async def handle_remove_key_phrases_request(message: Message, state: FSMContext) -> None:
    await state.set_state(KeyPhrasesStates.REMOVE_KEY_PHRASES)
    await message.reply('Please, send list of key phrases separated by new line')


@router.message(KeyPhrasesStates.ADD_KEY_PHRASES)
async def remove_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        removed_key_phrases = message.text.split('\n')
        async with KeyPhrasesDB(DB_NAME) as db:
            await db.key_phrase_init()
            all_key_phrases = await db.key_phrases_get(message.chat.id)
            for phrase in removed_key_phrases:
                if phrase in all_key_phrases:
                    await db.key_phrase_remove(message.chat.id, phrase)
            all_key_phrases = await db.key_phrases_get(message.chat.id)

        await state.set_state(KeyPhrasesStates.SEARCH_KEY_PHRASES)
        await message.reply(f'Key phrases have been removed\n\n{markdown.hitalic('Current list:\n')}'
                            f'{'\n'.join(all_key_phrases)}')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')


@router.message()
async def handle_kw(message: Message, state: FSMContext) -> None:
    # global detected_message, answering_photo_message
    key_phrase_manager.set_message(message)
    cur_detected_message = await key_phrase_manager.detect_kw()
    if cur_detected_message:
        core.detected_message = cur_detected_message
        core.answering_message =  await core.detected_message.reply('A suspicious message')  # await core.detected_message.reply_photo(BAD_WORDS)
        await key_phrase_manager.info_admins()
