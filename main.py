import asyncio

from typing import Callable

from functools import wraps

import logging

from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, CallbackQuery, ChatPermissions
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.filters import Command, CommandStart
from aiogram.utils import keyboard, markdown
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ParseMode, ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

import pymorphy3

HAMSTER_COMBAT = FSInputFile('attachments/hamster-combat.jpg')
ADMIN_GIF = FSInputFile('attachments/admin.mp4')
BAD_WORDS = FSInputFile('attachments/bad-words.jpg')
SORRY_SHREK = FSInputFile('attachments/sorry-shrek.jpg')

KEY_PHRASES = (
    'пассивный заработок',
    'источник заработок',
    'стабильный заработок',
    'регулярный заработок',
    'пассивный доход',
    'источник доход',
    'стабильный доход',
    'регулярный доход',
    'пассивный прибыль',
    'источник прибыль',
    'стабильный прибыль',
    'регулярный прибыль',
    'набор в команда',
    'удаленная занятость',
    'удаленный формат',
    'удаленный основа',
    'удалленный работа'
    'человек в команда',
    'писать в лс',
    'писать + в лс',
    'писать в личный сообщение',
    'писать + в личный сообщение',
    'только для совершеннолетний',
    '18+',
    'только для ответственный человек',
    'только для серьезный человек',
    'крипто',
    'крипта',
    'криптовалюта'
)

MUTE_DURATION = timedelta(seconds=31)

# krafter_msg_link = 'https://t.me/c/2180766004/7'
# admin_id = ''

# cur_session = aiogram.client.session.aiohttp.AiohttpSession(proxy='http://proxy.server:3128')
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
morph = pymorphy3.MorphAnalyzer()
dispatcher = Dispatcher()

# group_admins = {'MrKrafter': 1127277755, 'evevtish': 1644081190}
kb_action_buttons = {
    'Ignore': 'ignore_massage',
    'Delete message': 'delete_message',
    'Mute user': 'mute_user',
    'Ban user': 'ban_user'
}

detected_message: Message = None
answering_photo_message: Message = None


class Informer:
    def __init__(self) -> None:
        # self._processed_message = processed_message
        self.MSG_NOT_FOUND = "Message isn't found"
        '''
        self.IGNORE_MSG = (f'{self.get_detected_message_url('Message')} from {self.get_user_name()} was '
                           f'{markdown.hunderline('ignored')}\n\n{self.get_detected_message_quote()}')
        self.DELETE_MSG = (f'Message from {self.get_user_name()} was {markdown.hunderline('deleted')}\n\n'
                           f'{self.get_detected_message_quote()}')
        self.MUTE_USR = (f'{self.get_user_name()} was {markdown.hunderline('muted')}\n\n'
                         f'{self.get_detected_message_quote()}')
        self.BAN_USR = (f'{self.get_user_name()} was {markdown.hunderline('banned')}\n\n'
                        f'{self.get_detected_message_quote()}')
        self.INFO_ADMINS = (f'{self.get_user_name()} says {self.get_detected_message_url('bad words')}\n\n'
                            f'{self.get_detected_message_quote()}')
        '''

    # def set_processed_message(self, processed_message: Message):
    #     self._processed_message = processed_message

    def get_msg_not_found_info(self) -> str:
        return self.MSG_NOT_FOUND

    def get_ignore_msg_info(self) -> str:
        return 'Message was ignored'
        # return (f'{self.get_detected_message_url('Message')} from {self.get_user_name()} was '
        #         f'{markdown.hunderline('ignored')}\n\n{self.get_detected_message_quote()}')

    def get_delete_msg_info(self) -> str:
        return 'Message was deleted'
        # return (f'Message from {self.get_user_name()} was {markdown.hunderline('deleted')}\n\n'
        #         f'{self.get_detected_message_quote()}')

    def get_mute_user_info(self) -> str:
        return 'User was muted'
        # return f'{self.get_user_name()} was {markdown.hunderline('muted')}\n\n{self.get_detected_message_quote()}'

    def get_ban_user_info(self) -> str:
        return 'User was banned'
        # return f'{self.get_user_name()} was {markdown.hunderline('banned')}\n\n{self.get_detected_message_quote()}'

    def get_info_for_admins(self) -> str:
        return 'Suspicious message was detected'
        # return (f'{self.get_user_name()} says {self.get_detected_message_url('bad words')}\n\n'
        #         f'{self.get_detected_message_quote()}')

    def use_safely(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args) -> str:
            result = self.MSG_NOT_FOUND
            try:
                result = func(self, *args)
            except AttributeError:
                pass
            return result

        return wrapper

    @use_safely
    def get_user_name(self) -> str:
        return f'{markdown.hbold(detected_message.from_user.full_name)} (@{detected_message.from_user.username})'

    @use_safely
    def get_detected_message_url(self, text: str) -> str:
        return markdown.hlink(text, detected_message.get_url())

    @use_safely
    def get_detected_message_quote(self) -> str:
        return markdown.hitalic('Message text:\n') + markdown.hblockquote(detected_message.text)


informer = Informer()


def convert_to_normal_form(phrase: str) -> str:
    normal_form_phrase = []
    try:
        for word in phrase.split():
            normal_form_phrase.append(morph.parse(word.strip())[0].normal_form)
    except AttributeError:
        pass
    return ' '.join(normal_form_phrase)


def create_inline_kb(buttons: dict) -> keyboard.InlineKeyboardMarkup:
    inline_kb_builder = keyboard.InlineKeyboardBuilder()
    for btn_text, btn_callback in buttons.items():
        inline_kb_builder.button(text=btn_text, callback_data=btn_callback)
    return inline_kb_builder.adjust(1).as_markup()


async def info_admins(message: Message) -> None:
    for cur_admin in await bot.get_chat_administrators(message.chat.id):
        if not cur_admin.user.is_bot:
            await bot.send_photo(
                cur_admin.user.id,
                HAMSTER_COMBAT,
                caption=informer.get_info_for_admins(),
                reply_markup=create_inline_kb(kb_action_buttons)
            )


'''
def detect_keywords(message: Message) -> Message:
    normal_form_key_phrase = convert_to_normal_form(message.text)
    for kw_phrase in KEY_PHRASES:
        if kw_phrase in normal_form_key_phrase:
            return message
'''


async def user_restricting_troubleshoot(callback: CallbackQuery) -> None:
    # temp_callback: CallbackQuery
    info_caption = ("This operation can't be done, probably this is because user is admin. Would you like to delete "
                    "message anyway?")
    ask_buttons = {
        'Yes': 'delete_message',
        'No': 'ignore_massage'
    }

    await callback.message.edit_caption(caption=info_caption, reply_markup=create_inline_kb(ask_buttons))
    if dispatcher.callback_query(F.data == 'delete_message'):
        await delete_message(CallbackQuery())
    elif dispatcher.callback_query(F.data == 'ignore_massage'):
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
                await answer_callback(informer.get_msg_not_found_info())

            except AttributeError:
                await answer_callback(informer.get_msg_not_found_info())

        return wrapper

    return decorator


@dispatcher.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer_animation(ADMIN_GIF)


@dispatcher.message(Command('help'))
async def handle_help(message: Message) -> None:
    await message.answer('*help*')


@dispatcher.message()
async def handle_keywords(message: Message) -> None:
    """
    normal_form_key_phrase = await convert_to_normal_form(message.text)
    for kw_phrase in key_phrases:
        if kw_phrase in normal_form_key_phrase:
            global bad_message
            bad_message = message
            # await message.reply_photo(hamster_combat, has_spoiler=True)
            await info_admins(message)
            return message
    """
    global detected_message, answering_photo_message
    normal_form_key_phrase = convert_to_normal_form(message.text)

    for kw_phrase in KEY_PHRASES:
        if kw_phrase in normal_form_key_phrase:
            detected_message = message
            answering_photo_message = await detected_message.reply_photo(BAD_WORDS, disable_notification=True)
            await info_admins(message)
            break


'''
@dispatcher.message(Command('addAdmin'))
async def add_admin(message: Message) -> None:
    bot.adm
    cur_username = message.from_user.username
    group_admins[cur_username] = message.from_user.id
    await message.answer(f'{get_user_name(message)} was added to admin list')
'''


@dispatcher.callback_query(F.data == 'ignore_massage')
@log_message_action(informer.get_ignore_msg_info())
async def ignore_message(callback: CallbackQuery) -> None:
    await answering_photo_message.edit_media(InputMediaPhoto(media=SORRY_SHREK))


@dispatcher.callback_query(F.data == 'delete_message')
@log_message_action(informer.get_delete_msg_info())
async def delete_message(callback: CallbackQuery) -> None:
    await bot.delete_message(detected_message.chat.id, detected_message.message_id)
    await bot.delete_message(answering_photo_message.chat.id, answering_photo_message.message_id)


@dispatcher.callback_query(F.data == 'mute_user')
@log_message_action(informer.get_mute_user_info(), use_troubleshooting=True)
async def mute_user(callback: CallbackQuery) -> None:
    await bot.restrict_chat_member(
        detected_message.chat.id,
        detected_message.from_user.id,
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


@dispatcher.callback_query(F.data == 'ban_user')
@log_message_action(informer.get_ban_user_info(), use_troubleshooting=True)
async def ban_user(callback: CallbackQuery) -> None:
    await bot.ban_chat_member(detected_message.chat.id, detected_message.from_user.id, revoke_messages=True)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
