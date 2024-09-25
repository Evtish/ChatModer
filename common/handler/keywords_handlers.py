from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

import common
from .. import text_or_caption
from ..config.settings import Callback, DB_NAME
from ..config.media import HAMSTER_COMBAT, BAD_WORDS
from ..informer.get_info_messages import get_info_for_admins
from common.key_phrases_db import KeyPhrasesDB

import pymorphy3

router = Router(name=__name__)
morph = pymorphy3.MorphAnalyzer()

kb_action_buttons = {
    'Ignore': Callback.IGNORE_MESSAGE,
    'Delete message': Callback.DELETE_MESSAGE,
    'Mute user': Callback.MUTE_USER,
    'Ban user': Callback.BAN_USER
}


def convert_to_normal_form(phrase: str) -> str:
    normal_form_phrase = []
    try:
        for word in phrase.split():
            normal_form_phrase.append(morph.parse(word.strip())[0].normal_form)
    except AttributeError:
        pass
    return ' '.join(normal_form_phrase)


async def detect_kw(message: Message) -> Message:
    async with KeyPhrasesDB(DB_NAME) as db:
        key_phrases = await db.key_phrases_get(message.chat.id)

    text_or_caption.set_message(message)
    normal_form_key_phrase = convert_to_normal_form(text_or_caption.get_text_or_caption())
    for kw_phrase in key_phrases:
        if kw_phrase in normal_form_key_phrase:
            return message


async def info_admins(message: Message) -> None:
    try:
        for cur_admin in await common.bot.get_chat_administrators(message.chat.id):
            if not cur_admin.user.is_bot:
                await common.bot.send_photo(
                    cur_admin.user.id,
                    HAMSTER_COMBAT,
                    caption=get_info_for_admins(),
                    reply_markup=common.create_inline_kb(kb_action_buttons)
                )
    except (AttributeError, TelegramBadRequest):
        pass


@router.message()
async def handle_kw(message: Message) -> None:
    # global detected_message, answering_photo_message
    cur_detected_message = await detect_kw(message)
    if cur_detected_message:
        common.detected_message = cur_detected_message
        common.answering_message = await common.detected_message.reply_photo(BAD_WORDS, disable_notification=True)
        await info_admins(message)

    '''
    for kw_phrase in KEY_PHRASES:
        if kw_phrase in normal_form_key_phrase:
            detected_message = message
            answering_photo_message = await detected_message.reply_photo(BAD_WORDS, disable_notification=True)
            await info_admins(message)
            break
    '''
