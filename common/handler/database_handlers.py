from aiogram import Router, F
from aiogram.types import Message, Chat, User

import sqlite3

from .. import bot, detected_message
from common.config.settings import KEY_PHRASES

router = Router(name=__name__)

db_connection = sqlite3.connect('main_database.db')
db_cursor = db_connection.cursor()


def get_chat_name_safety(name: str) -> str:
    return ''.join(s for s in name if s.isalnum())


@router.message(F.new_chat_member)
async def new_member(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        table_name = get_chat_name_safety(message.chat.full_name)
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS key_phrases (
                                chat_id INTEGER,
                                chat_fullname TEXT,
                                admin_list TEXT,
                                kw_list TEXT
                            )''')
        db_connection.commit()

        db_cursor.execute('INSERT INTO key_phrases (chat_id, chat_fullname) VALUES (?, ?)', (
                            message.chat.id,
                            get_chat_name_safety(message.chat.full_name))
                          )

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
