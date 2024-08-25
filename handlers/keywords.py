from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

import pymorphy3

from informer.info_messages import get_info_for_admins

import common

from config.settings import KEY_PHRASES
from config.media import HAMSTER_COMBAT, BAD_WORDS

router = Router(name=__name__)
morph = pymorphy3.MorphAnalyzer()

kb_action_buttons = {
    'Ignore': 'ignore_massage',
    'Delete message': 'delete_message',
    'Mute user': 'mute_user',
    'Ban user': 'ban_user'
}


def convert_to_normal_form(phrase: str) -> str:
    normal_form_phrase = []
    try:
        for word in phrase.split():
            normal_form_phrase.append(morph.parse(word.strip())[0].normal_form)
    except AttributeError:
        pass
    return ' '.join(normal_form_phrase)


def detect_kw(message: Message) -> Message:
    normal_form_key_phrase = convert_to_normal_form(message.text)
    for kw_phrase in KEY_PHRASES:
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
    common.detected_message = detect_kw(message)
    common.answering_photo_message = await common.detected_message.reply_photo(BAD_WORDS, disable_notification=True)
    await info_admins(message)

    '''
    for kw_phrase in KEY_PHRASES:
        if kw_phrase in normal_form_key_phrase:
            detected_message = message
            answering_photo_message = await detected_message.reply_photo(BAD_WORDS, disable_notification=True)
            await info_admins(message)
            break
    '''
