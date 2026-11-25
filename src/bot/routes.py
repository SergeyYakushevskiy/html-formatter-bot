import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InputRichMessage, Message

from services.locale import MessageProvider

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, message_provider: MessageProvider):
    try:
        await message.answer(message_provider.get("start"))
    except Exception as e:
        logger.error("Failed to send message. %s", e)


@router.message(Command("help"))
async def help_handler(message: Message, message_provider: MessageProvider):
    try:
        await message.answer(message_provider.get("help"))
    except Exception as e:
        logger.error("Failed to send message. %s", e)


@router.message(F.text)
async def message_handler(message: Message) -> None:
    try:
        await message.answer_rich(rich_message=InputRichMessage(html=message.text))
        logger.info(
            "New message from @%s (ID: %s)",
            message.from_user.username or message.from_user.full_name,
            message.from_user.id,
        )
    except Exception as e:
        logger.error("Failed to format or send message. %s", e)
