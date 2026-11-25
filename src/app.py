import asyncio
import logging
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from bot.bot import Bot
from config.config import Settings
from gui.controller import Controller
from gui.event import EventStream
from gui.gui import GUI
from log.config import LoggingConfig
from services.locale import MessageProvider

logger = logging.getLogger(__name__)


def main():
    settings = Settings()
    event_stream = EventStream()
    LoggingConfig.setup_logging(settings, event_stream)

    logger.debug("Application startup...")

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    logger.debug("Import locales...")
    mp = MessageProvider(settings)

    logger.debug("Initializing bot...")
    bot = Bot(settings, mp)

    logger.debug("Create user interface...")
    gui = GUI(settings, event_stream)

    controller = Controller(bot, settings, gui)

    gui.show()

    logger.info("Application startup completed")

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
