from aiogram import Router, F
from aiogram.types import Message, Chat, User

import sqlite3

from .. import bot, detected_message
from common.config.settings import KEY_PHRASES

router = Router(name=__name__)

db_connection = sqlite3.connect('key_phrases.db')
db_cursor = db_connection.cursor()


def get_chat_name_safety(name: str) -> str:
    return ''.join(s for s in name if s.isalnum())


@router.message(F.new_chat_member)
async def new_member(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        await message.answer('skibidi51')

        table_name = get_chat_name_safety(message.chat.full_name)
        table_creation_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                        chat_data TEXT,
                        kw_list TEXT,
                        admin_list TEXT
                    )'''
        db_cursor.execute(table_creation_query)
        db_connection.commit()

        data_inserting_query = f'INSERT INTO {table_name} (chat_data) VALUES (?)'
        db_cursor.execute(data_inserting_query, ('repr(message.chat)',))

# def get_common_chats(user_id: int | str) -> list[Chat]:
#     chats = db_cursor.execute('SELECT ')


# @router.message(F.text == 'skibidi')
# def add_keyword(message: Message) -> None:
#     if detected_message:
#         db_cursor.execute('INSERT INTO key_phrase VALUES (?, "skibidi")', str(detected_message.chat.id))
#         db_connection.commit()
#         res = db_cursor.execute('SELECT chat, kw_list FROM key_phrase')
#         message.answer('hype')
#         message.answer('\n'.join(res.fetchall()))