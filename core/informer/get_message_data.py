from functools import wraps
from typing import Callable

from aiogram.utils import markdown

from core.informer import EXECUTION_ERROR_TEXT
from core import detected_message


def use_safely(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        result = EXECUTION_ERROR_TEXT
        try:
            result = func(*args, **kwargs)
        except AttributeError:
            pass
        return result

    return wrapper


@use_safely
def get_user_name() -> str:
    return f'{markdown.hbold(detected_message.from_user.full_name)} (@{detected_message.from_user.username})'


@use_safely
def get_detected_message_url(text: str) -> str:
    return markdown.hlink(text, detected_message.get_url())


@use_safely
def get_detected_message_quote() -> str:
    return markdown.hitalic('Message text:\n') + markdown.hblockquote(detected_message.text)


__all__ = (
    'get_user_name',
    'get_detected_message_url',
    'get_detected_message_quote'
)