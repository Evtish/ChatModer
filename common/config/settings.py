from enum import Enum
from os import getenv
from datetime import timedelta

BOT_TOKEN = getenv('BOT_TOKEN')

MUTE_DURATION = timedelta(seconds=31)

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
    'удаленный работа'
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


class Callback(Enum):
    IGNORE_MESSAGE = 'ignore_massage',
    DELETE_MESSAGE = 'delete_message',
    MUTE_USER = 'mute_user',
    BAN_USER = 'ban_user',
    EDIT_TEXT = 'edit_text',
    EDIT_CAPTION = 'edit_caption'
