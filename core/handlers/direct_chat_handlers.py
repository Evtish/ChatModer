from datetime import datetime
from functools import wraps
from typing import Callable

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto, ChatPermissions

import core
from .. import create_inline_kb, message_manager
from system.settings import MUTE_DURATION, Callback
from system.media import SORRY_SHREK
from ..informer.get_info_messages import *

router = Router(name=__name__)


async def user_restricting_troubleshoot(callback: CallbackQuery) -> None:
    # temp_callback: CallbackQuery
    info_text = ("This operation can't be done, probably this is because user is admin. Would you like to delete "
                 "message anyway?")
    ask_buttons = {
        'Yes': Callback.DELETE_MESSAGE,
        'No': Callback.IGNORE_MESSAGE
    }

    # message_manager.set_message(callback.message)
    # await message_manager.edit_text_or_caption(info_text, new_markup=create_inline_kb(ask_buttons))
    await callback.message.edit_text(info_text, reply_markup=create_inline_kb(ask_buttons))
    if router.callback_query(F.data == Callback.DELETE_MESSAGE):
        await delete_message(CallbackQuery())
    elif router.callback_query(F.data == Callback.IGNORE_MESSAGE):
        await ignore_message(CallbackQuery())


def log_message_action(info: str, use_troubleshooting: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(callback: CallbackQuery) -> None:
            async def answer_callback(text: str) -> None:
                await callback.answer()
                message_manager.set_message(callback.message)
                await message_manager.edit_text_or_caption(text)

            try:
                returned_func = await func(callback)
                await answer_callback(info)
                return returned_func

            except TelegramBadRequest:
                if use_troubleshooting:
                    return await user_restricting_troubleshoot(callback)
                await answer_callback(get_not_found_message())

            except AttributeError:
                await answer_callback(get_not_found_message())

        return wrapper

    return decorator


@router.callback_query(F.data == Callback.IGNORE_MESSAGE)
@log_message_action(get_ignore_message())
async def ignore_message(callback: CallbackQuery) -> None:
    try:
        await core.answering_message.edit_text('Sorry, this message is OK')
        # await core.answering_message.edit_media(InputMediaPhoto(media=SORRY_SHREK))
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == Callback.DELETE_MESSAGE)
@log_message_action(get_delete_message())
async def delete_message(callback: CallbackQuery) -> None:
    await core.detected_message.delete()
    await core.answering_message.delete()


@router.callback_query(F.data == Callback.MUTE_USER)
@log_message_action(get_mute_message(), use_troubleshooting=True)
async def mute_user(callback: CallbackQuery) -> None:
    await core.bot.restrict_chat_member(
        core.detected_message.chat.id,
        core.detected_message.from_user.id,
        ChatPermissions(
            can_send_messages=False,
            can_send_photos=False,
            can_send_videos=False,
            can_send_video_notes=False,
            can_send_audios=False,
            can_send_voice_notes=False,
            can_send_documents=False,
            can_send_polls=False,
            can_send_other_messages=False
        ),
        until_date=datetime.now() + MUTE_DURATION
    )
    await delete_message(F)


@router.callback_query(F.data == Callback.BAN_USER)
@log_message_action(get_ban_message(), use_troubleshooting=True)
async def ban_user(callback: CallbackQuery) -> None:
    await core.bot.ban_chat_member(
        core.detected_message.chat.id,
        core.detected_message.from_user.id,
        revoke_messages=True
    )
