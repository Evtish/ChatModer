import string
from enum import StrEnum
from os import getenv
from datetime import timedelta

from aiogram.fsm.state import StatesGroup, State

BOT_TOKEN = getenv('BOT_TOKEN')
DB_NAME = 'main_database.db'
MUTE_DURATION = timedelta(seconds=31)
CORRECT_SYMBOLS = string.printable + ''.join(map(lambda c: chr(c), range(ord('А'), ord('я')))) + 'ёЁ'

# KEY_PHRASES = (
#     'пассивный заработок',
#     'источник заработок',
#     'стабильный заработок',
#     'регулярный заработок',
#     'пассивный доход',
#     'источник доход',
#     'стабильный доход',
#     'регулярный доход',
#     'пассивный прибыль',
#     'источник прибыль',
#     'стабильный прибыль',
#     'регулярный прибыль',
#     'набор в команда',
#     'удаленная занятость',
#     'удаленный формат',
#     'удаленный основа',
#     'удаленный работа'
#     'человек в команда',
#     'писать в лс',
#     'писать + в лс',
#     'писать в личный сообщение',
#     'писать + в личный сообщение',
#     'только для совершеннолетний',
#     '18+',
#     'только для ответственный человек',
#     'только для серьезный человек',
#     'крипто',
#     'крипта',
#     'криптовалюта'
# )


class Callback(StrEnum):
    IGNORE_MESSAGE: str = 'ignore_massage',
    DELETE_MESSAGE: str = 'delete_message',
    MUTE_USER: str = 'mute_user',
    BAN_USER: str = 'ban_user',
    EDIT_TEXT: str = 'edit_text',
    EDIT_CAPTION: str = 'edit_caption'


class KeyPhrasesStates(StatesGroup):
    SEARCH_KEY_PHRASES = State()
    ADD_KEY_PHRASES = State()
    REMOVE_KEY_PHRASES = State()