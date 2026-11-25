import logging
from datetime import datetime
from pathlib import Path
import sys
from typing import TextIO

from config.config import Settings


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
        log_dir = Path(settings.log.dir)
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
