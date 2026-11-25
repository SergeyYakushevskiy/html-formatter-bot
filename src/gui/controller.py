import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

from bot.bot import Bot
from config.config import Settings
from gui.gui import GUI

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self, bot: Bot, settings: Settings, gui: GUI):
        self.bot = bot
        self.settings = settings
        self.gui = gui

        self._connect_signals()

    def _connect_signals(self) -> None:
        try:
            self.gui.start_requested.connect(
                lambda: self._create_task(self._start_bot())
            )
            self.gui.stop_requested.connect(lambda: self._create_task(self._stop_bot()))
            self.gui.restart_requested.connect(
                lambda: self._create_task(self._restart_bot())
            )
            self.gui.token_accepted.connect(
                lambda token: self._create_task(self._update_token(token))
            )
            self.gui.exit_requested.connect(
                lambda: self._create_task(self._exit_application())
            )
        except Exception:
            logger.exception("Failed to connect signals")

    def _create_task(self, coroutine: Coroutine[Any, Any, Any]) -> None:
        task = asyncio.create_task(coroutine)
        task.add_done_callback(self._handle_task_result)

    @staticmethod
    def _handle_task_result(task: asyncio.Task) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            logger.debug("Controller task cancelled")
        except Exception:
            logger.exception("Controller task failed")

    async def _start_bot(self) -> None:
        await self.bot.start()
        self.gui.set_running(self.bot.running)

    async def _stop_bot(self) -> None:
        await self.bot.stop()
        self.gui.set_running(self.bot.running)

    async def _restart_bot(self) -> None:
        await self.bot.stop()
        await self.bot.start()

    async def _update_token(self, token: str) -> None:
        try:
            self.settings.bot.update_token(token)
        except ValueError:
            logger.exception("Failed to update token")
            return

        await self.bot.stop()
        await self.bot.start(token)

    async def _exit_application(self) -> None:
        try:
            await self.bot.stop()
        finally:
            self.gui.close()
