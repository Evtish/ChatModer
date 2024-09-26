# from aiosqlite import Connection, Cursor
#
#
# class BaseTable:
#     def __init__(self, db_connection: Connection, db_cursor: Cursor) -> None:
#         chat_id: str
#         self.db_connection = db_connection
#         self.db_cursor = db_cursor
#
#     async def add_line(self, *args):
#         pass
#
#     async def remove_line(self, *args):
#         pass
#
#     async def get_table(self, *args):
#         pass
#
#
# class ChatTable(BaseTable):
#     def __init__(self, db_connection: Connection, db_cursor: Cursor) ->:
#         super().__init__(db_connection, db_cursor)
#         chat_fullname: str
#
#     async def __aenter__(self):
#         await self.db_cursor.execute('''
#             CREATE TABLE IF NOT EXISTS chats (
#                 chat_id INTEGER,
#                 chat_fullname TEXT
#             )
#         ''')
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#     async def add_line(self, chat_fullname: str):
#         await self.db_cursor.execute('INSERT OR REPLACE INTO chats (chat_id, safe_chat_fullname) VALUES (?, ?)', (
#             chat_id,
#             chat_fullname
#         ))
#         await self.database_backend.commit()
