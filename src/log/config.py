import logging
from datetime import datetime
import os
from pathlib import Path
import sys
from typing import TextIO

from config import ROOT_DIR
from config.config import Settings


def get_log_dir() -> Path:
    match sys.platform:
        case "win32":
            base_dir = Path(os.environ["LOCALAPPDATA"])
        case "linux":
            base_dir = Path(
                os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")
            )
        case _:
            raise OSError(f"Unsupported operating system: {sys.platform}")

    return base_dir / "html-formatter-bot"


LOG_DIR = get_log_dir()


class LoggingConfig:
    @staticmethod
    def setup_logging(settings: Settings, out_stream: TextIO) -> None:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler
        log_dir = Path(LOG_DIR / "html-formatter-bot")
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / f"{datetime.now():%Y-%m-%d}.log",
            encoding="utf-8",
            delay=True,
        )
        file_handler.setLevel(logging.CRITICAL)
        file_handler.setFormatter(formatter)

        # Stream handler
        stream_handler = logging.StreamHandler(out_stream)
        stream_handler.setLevel(settings.log.level.upper())
        stream_handler.setFormatter(formatter)

        # Stdout handler
        debug_handler = logging.StreamHandler(sys.stdout)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
        debug_handler.setFormatter(formatter)

        # Configure root logger
        logger.handlers.clear()
        logger.addHandler(file_handler)
        logger.addHandler(debug_handler)
        logger.addHandler(stream_handler)
