# __all__ = {'main_router'}

from aiogram import Router
from aiogram.types import Message
from aiogram.utils import keyboard

from .base import router as base_router
from .admin import router as admin_router
from .keywords import router as keywords_router


def create_inline_kb(buttons: dict) -> keyboard.InlineKeyboardMarkup:
    inline_kb_builder = keyboard.InlineKeyboardBuilder()
    for btn_text, btn_callback in buttons.items():
        inline_kb_builder.button(text=btn_text, callback_data=btn_callback)
    return inline_kb_builder.adjust(1).as_markup()


class TextOrCaption:
    def __init__(self, message: Message) -> None:
        self.message = message

    def set_message(self, message: Message) -> None:
        self.message = message

    def get_text_or_caption(self) -> str:
        if self.message.text:
            return self.message.text
        elif self.message.caption:
            return self.message.caption

    async def edit_text_or_caption(self, new_text: str) -> None:
        if self.message.text:
            await self.message.edit_text(new_text)
        elif self.message.caption:
            await self.message.edit_caption(caption=new_text)


main_router = Router(name=__name__)
main_router.include_routers(base_router, admin_router)

main_router.include_router(keywords_router)  # must be the latest
