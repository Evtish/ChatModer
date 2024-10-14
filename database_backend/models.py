from sqlalchemy.orm import Mapped

from database_backend import Base


class ParentModel(Base):
    chat_id: Mapped[int]


class Chat(ParentModel):
    chat_fullname: Mapped[str]


class KeyPhrase(ParentModel):
    key_phrase: Mapped[str]


class DetectedMessage(ParentModel):
    chat_fullname: Mapped[str]
    message_id: Mapped[int]
    message_text: Mapped[str]
    message_link: Mapped[str]
    author_id: Mapped[int]
    author_username: Mapped[str]
    author_fullname: Mapped[str]