from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

from system.settings import CORRECT_SYMBOLS


def get_safe_text(name: str) -> str:
    return ''.join(s for s in name if s in CORRECT_SYMBOLS)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + 's'
