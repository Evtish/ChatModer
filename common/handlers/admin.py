from datetime import datetime
from functools import wraps
from typing import Callable

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto, ChatPermissions

import common
import common.handlers
from common.config.settings import MUTE_DURATION, Callback
from common.config.media import SORRY_SHREK
from common.informer.get_info_messages import *

router = Router(name=__name__)


async def user_restricting_troubleshoot(callback: CallbackQuery) -> None:
    # temp_callback: CallbackQuery
    info_caption = ("This operation can't be done, probably this is because user is admin. Would you like to delete "
                    "message anyway?")
    ask_buttons = {
        'Yes': Callback.DELETE_MESSAGE,
        'No': Callback.IGNORE_MESSAGE
    }

    await callback.message.edit_caption(caption=info_caption, reply_markup=common.handlers.create_inline_kb(ask_buttons))
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
                await callback.message.edit_caption(caption=text)

            try:
                returned_func = await func(callback)
                await answer_callback(info)
                return returned_func

            except TelegramBadRequest:
                if use_troubleshooting:
                    return await user_restricting_troubleshoot(callback)
                await answer_callback(get_msg_not_found_info())

            except AttributeError:
                await answer_callback(get_msg_not_found_info())

        return wrapper

    return decorator


@router.callback_query(F.data == 'ignore_massage')
@log_message_action(get_ignore_msg_info())
async def ignore_message(callback: CallbackQuery) -> None:
    await common.answering_photo_message.edit_media(InputMediaPhoto(media=SORRY_SHREK))


@router.callback_query(F.data == 'delete_message')
@log_message_action(get_delete_msg_info())
async def delete_message(callback: CallbackQuery) -> None:
    await common.detected_message.delete()
    await common.answering_photo_message.delete()


@router.callback_query(F.data == 'mute_user')
@log_message_action(get_mute_user_info(), use_troubleshooting=True)
async def mute_user(callback: CallbackQuery) -> None:
    await common.bot.restrict_chat_member(
        common.detected_message.chat.id,
        common.detected_message.from_user.id,
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


@router.callback_query(F.data == 'ban_user')
@log_message_action(get_ban_user_info(), use_troubleshooting=True)
async def ban_user(callback: CallbackQuery) -> None:
    await common.bot.ban_chat_member(
        common.detected_message.chat.id,
        common.detected_message.from_user.id,
        revoke_messages=True
    )
