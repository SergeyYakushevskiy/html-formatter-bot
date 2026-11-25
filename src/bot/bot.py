import asyncio
import logging

from aiogram import Bot as AiogramBot, Dispatcher

from config.config import Settings
from services.locale import MessageProvider
from bot.routes import router

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, settings: Settings, message_provider: MessageProvider):
        self.settings = settings

        self._token = settings.bot.token
        self.bot = AiogramBot(self._token)
        self.dp = Dispatcher()

        self.dp["message_provider"] = message_provider
        self.dp.include_router(router)

        self._task: asyncio.Task | None = None
        self.running: bool = False

    async def start(self, token: str | None = None) -> None:
        logger.debug("Bot startup...")

        try:
            if self._task is not None and not self._task.done():
                return

            if token and token != self._token:
                self._token = token
                self.bot = AiogramBot(self._token)

            self._task = asyncio.create_task(self.dp.start_polling(self.bot))
            self.running = True
            logger.info("Bot startup completed")

        except Exception:
            logger.exception("Failed to start bot")

    async def stop(self) -> None:
        logger.debug("Bot stopping...")

        try:
            if self._task is None:
                return

            if not self._task.done():
                await self.dp.stop_polling()

            await self._task
            await self.bot.session.close()

            self._task = None

            logger.info("Bot stopped")
            self.running = False
        except Exception:
            logger.exception("Failed to stop bot")
