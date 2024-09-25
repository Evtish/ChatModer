from pathlib import Path
from typing import Self

import string
import asyncio

import aiosqlite


def get_safe_chat_name(name: str) -> str:
    return ''.join(s for s in name if s in string.printable)


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

    async def add_chat_id(self, chat_id: int) -> None:
        async with self.lock:
            await self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS key_phrases (
                    chat_id INTEGER,
                    chat_fullname TEXT,
                    kw_list TEXT
                )
            ''')

            await self.db_cursor.execute('INSERT OR REPLACE INTO key_phrases (chat_id) VALUES (?)', (chat_id,))
            await self.database.commit()

    async def add_chat_fullname(self, chat_id: int, chat_fullname: str) -> None:
        safe_chat_fullname = get_safe_chat_name(chat_fullname)
        async with self.lock:
            await self.db_cursor.execute(
                'UPDATE key_phrases SET (chat_fullname) = (?) WHERE chat_id = (?)',
                (safe_chat_fullname, chat_id)
            )
            await self.database.commit()

    async def remove_chat(self, chat_id: int) -> None:
        async with self.lock:
            await self.db_cursor.execute('DELETE FROM key_phrases WHERE chat_id = (?)', (chat_id,))
            await self.database.commit()
