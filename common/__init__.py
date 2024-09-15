from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils import keyboard

from common.config.settings import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

detected_message: Message | None = None
answering_message: Message | None = None


def create_inline_kb(buttons: dict) -> keyboard.InlineKeyboardMarkup:
    inline_kb_builder = keyboard.InlineKeyboardBuilder()
    for btn_text, btn_callback in buttons.items():
        inline_kb_builder.button(text=btn_text, callback_data=btn_callback)
    return inline_kb_builder.adjust(1).as_markup()


class TextOrCaption:
    message: Message

    def set_message(self, message: Message) -> None:
        self.message = message

    def get_text_or_caption(self) -> str:
        if self.message.text:
            return self.message.text
        elif self.message.caption:
            return self.message.caption

    async def edit_text_or_caption(self, new_text: str, new_markup: InlineKeyboardMarkup | None = None) -> None:
        if self.message.text:
            await self.message.edit_text(new_text)
        elif self.message.caption:
            await self.message.edit_caption(caption=new_text, reply_markup=new_markup)


text_or_caption = TextOrCaption()
