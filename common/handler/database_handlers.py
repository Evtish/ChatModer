from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import sqlite3

from .. import bot
from ..config.settings import KeyPhrasesStates

router = Router(name=__name__)

main_db = sqlite3.connect('main_database.db', check_same_thread=False)
main_db_cursor = main_db.cursor()


def get_chat_name_safety(name: str) -> str:
    return ''.join(s for s in name if s.isalnum())


@router.message(F.new_chat_member)
def add_chat_to_db(message: Message) -> None:
    if bot.id in map(lambda user: user.id, message.new_chat_members):
        main_db_cursor.execute('''CREATE TABLE IF NOT EXISTS key_phrases (
                                    chat_id INTEGER,
                                    chat_fullname TEXT,
                                    admin_list TEXT,
                                    kw_list TEXT
                                )''')

        main_db_cursor.execute('INSERT INTO key_phrases (chat_id, chat_fullname) VALUES (?, ?)', (
            message.chat.id,
            get_chat_name_safety(message.chat.full_name))
                               )
        main_db.commit()


@router.message(F.left_chat_member)
def remove_chat_from_db(message: Message) -> None:
    if message.left_chat_member.id == bot.id:
        main_db_cursor.execute('DELETE FROM key_phrases WHERE chat_id = (?)', (message.chat.id,))
        main_db.commit()


@router.message(Command('banwords'))
async def handle_key_phrases_request(message: Message, state: FSMContext) -> None:
    if message.from_user in map(lambda member: member.user, await bot.get_chat_administrators(message.chat.id)):
        await state.set_state(KeyPhrasesStates.WAIT_FOR_KEY_PHRASES)
        await message.reply('Please, send list of key phrases separated by new line')
    else:
        await message.reply('This command is for admins only')


@router.message(KeyPhrasesStates.WAIT_FOR_KEY_PHRASES)
async def get_key_phrases(message: Message, state: FSMContext) -> None:
    try:
        get_key_phrases.key_phrases = message.text.split('\n')
        # await state.update_data(key_phrases=message.text.split('\n'))
        await state.clear()
        await message.reply('Key phrases have been set')
        print(*get_key_phrases.key_phrases, sep='\n')
    except AttributeError:
        await message.reply('Invalid key phrases. Please, try again')
