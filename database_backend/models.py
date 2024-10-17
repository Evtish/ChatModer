from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database_backend import Base


class Parent(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class Chat(Parent):
    # id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    chat_fullname: Mapped[str]


class KeyPhrase(Parent):
    # id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.chat_id', ondelete='CASCADE'))
    key_phrase: Mapped[str]


class DetectedMessage(Parent):
    # id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.chat_id', ondelete='CASCADE'))
    chat_fullname: Mapped[str]
    message_id: Mapped[int]
    message_text: Mapped[str]
    message_link: Mapped[str]
    author_id: Mapped[int]
    author_username: Mapped[str]
    author_fullname: Mapped[str]