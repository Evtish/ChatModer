# from aiogram.utils import markdown

from . import EXECUTION_ERROR_TEXT
# from .get_message_data import *


def get_not_found_message() -> str:
    return EXECUTION_ERROR_TEXT


def get_ignore_message() -> str:
    return 'Message was ignored'
    # return (f'{get_detected_message_url('Message')} from {get_user_name()} was '
    #         f'{markdown.hunderline('ignored')}\n\n{get_detected_message_quote()}')


def get_delete_message() -> str:
    return 'Message was deleted'
    # return (f'Message from {get_user_name()} was {markdown.hunderline('deleted')}\n\n'
    #         f'{get_detected_message_quote()}')


def get_mute_message() -> str:
    return 'User was muted'
    # return f'{get_user_name()} was {markdown.hunderline('muted')}\n\n{get_detected_message_quote()}'


def get_ban_message() -> str:
    return 'User was banned'
    # return f'{get_user_name()} was {markdown.hunderline('banned')}\n\n{get_detected_message_quote()}'


def get_for_admins_message() -> str:
    return 'Suspicious message was detected'
    # return (f'{get_user_name()} says {get_detected_message_url('bad words')}\n\n'
    #         f'{get_detected_message_quote()}')
