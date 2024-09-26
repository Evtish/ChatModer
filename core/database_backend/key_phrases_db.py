from core.config.settings import CORRECT_SYMBOLS

from pathlib import Path
from typing import Self, Iterator

import asyncio
import aiosqlite


def get_safe_text(name: str) -> str:
    return ''.join(s for s in name if s in CORRECT_SYMBOLS)


class KeyPhrasesDB:
    def __init__(self, db_file: Path | str) -> None:
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self) -> Self:
        self.database = await aiosqlite.connect(self.db_file, check_same_thread=False)
        self.db_cursor = await self.database.cursor()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.db_cursor.close()
        await self.database.close()

    async def chat_init(self):
        await self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER,
                chat_fullname TEXT,
                UNIQUE(chat_id)
            )
        ''')

    async def chat_add(self, chat_id: int, chat_fullname: str) -> None:
        async with self.lock:
            safe_chat_fullname = get_safe_text(chat_fullname)
            await self.db_cursor.execute('INSERT OR REPLACE INTO chats (chat_id, chat_fullname) VALUES (?, ?)', (
                chat_id,
                safe_chat_fullname
            ))
            await self.database.commit()

    async def chat_remove(self, chat_id: int) -> None:
        async with self.lock:
            await self.db_cursor.execute('DELETE FROM chats WHERE chat_id = (?)', (chat_id,))
            await self.database.commit()

    # async def admin_init(self):
    #     await self.db_cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS admins (
    #             chat_id INTEGER,
    #             admin_id INTEGER,
    #             admin_username TEXT,
    #             admin_fullname TEXT,
    #             can_delete_msg INTEGER,
    #             can_restrict_user INTEGER
    #         )
    #     ''')
    #
    # async def admin_add(
    #         self,
    #         chat_id: int,
    #         admin_id: int,
    #         admin_username: str,
    #         admin_fullname: str,
    #         can_delete_msg: bool,
    #         can_restrict_user: bool
    # ) -> None:
    #     await self.db_cursor.execute('''
    #         INSERT OR REPLACE INTO admins (
    #             chat_id,
    #             admin_id,
    #             admin_username,
    #             admin_fullname,
    #             can_delete_msg,
    #             can_restrict_user
    #         ) VALUES (?, ?, ?, ?, ?, ?)''', (
    #         chat_id,
    #         admin_id,
    #         admin_username,
    #         admin_fullname,
    #         can_delete_msg,
    #         can_restrict_user
    #     ))
    #     await self.database_backend.commit()
    #
    # async def admin_remove(self, admin_id: int) -> None:
    #     async with self.lock:
    #         await self.db_cursor.execute('DELETE FROM admins WHERE admin_id = (?)', (admin_id,))
    #         await self.database_backend.commit()

    async def key_phrase_init(self):
        await self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_phrases (
                chat_id INTEGER,
                key_phrase TEXT
            )
        ''')

    async def key_phrase_add(self, chat_id: int, key_phrase: str) -> None:
        cur_chat_key_phrases = list(await self.key_phrases_get(chat_id))
        async with self.lock:
            safe_key_phrase = get_safe_text(key_phrase)
            if safe_key_phrase not in cur_chat_key_phrases:
                await self.db_cursor.execute('INSERT OR REPLACE INTO key_phrases (chat_id, key_phrase) VALUES (?, ?)', (
                    chat_id,
                    safe_key_phrase
                ))
                await self.database.commit()

    async def key_phrase_remove(self, chat_id: int, key_phrase: str) -> None:
        async with self.lock:
            await self.db_cursor.execute('DELETE FROM key_phrases WHERE chat_id = (?) AND key_phrase = (?)', (
                chat_id,
                key_phrase
            ))
            await self.database.commit()

    async def key_phrases_get(self, chat_id: int) -> Iterator[str]:
        async with self.lock:
            key_phrases_lines = await self.db_cursor.execute(
                'SELECT key_phrase FROM key_phrases WHERE chat_id = (?)',
                (chat_id,)
            )

            return map(lambda tup: tup[0], await key_phrases_lines.fetchall())

    async def detected_message_init(self):
        await self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_messages (
                chat_id: INTEGER,
                chat_fullname: TEXT,
                message_id: INTEGER,
                message_text: TEXT,
                message_link: TEXT,
                author_id: INTEGER,
                author_username: TEXT,
                author_fullname: TEXT,
                UNIQUE(chat_id, message_id)
            )
        ''')

    async def detected_message_add(
            self,
            chat_id: int,
            chat_fullname: str,
            message_id: int,
            message_text: str,
            message_link: str,
            author_id: int,
            author_username: str,
            author_fullname: str
    ) -> None:
        async with self.lock:
            await self.db_cursor.execute('''
                INSERT OR REPLACE INTO detected_messages (
                    chat_id,
                    chat_fullname,
                    message_id, 
                    message_text
                    message_link,
                    author_id,
                    author_username,
                    author_fullname
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                chat_id,
                chat_fullname,
                message_id,
                message_text,
                message_link,
                author_id,
                author_username,
                author_fullname
            ))
            await self.database.commit()

    async def detected_message_remove(self, chat_id: int, message_id: int) -> None:
        async with self.lock:
            await self.db_cursor.execute('DELETE FROM detected_messages WHERE chat_id = (?) AND message_id = (?)', (
                chat_id,
                message_id
            ))
            await self.database.commit()
