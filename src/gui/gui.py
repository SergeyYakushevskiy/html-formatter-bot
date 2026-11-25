from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout

from config import ASSETS_DIR
from config.config import Settings
from gui.dialog import TokenDialog
from gui.event import EventStream
from gui.menu import Menu


class GUI(QMainWindow):
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    restart_requested = pyqtSignal()
    token_accepted = pyqtSignal(str)
    exit_requested = pyqtSignal()

    def __init__(self, settings: Settings, event_stream: EventStream):
        super().__init__()

        self.settings = settings

        self.setWindowTitle(f"{settings.app.name} {settings.app.version}")
        self.setFixedSize(640, 480)

        self._setup_ui(event_stream)
        self._connect_signals()
        logo_path = ASSETS_DIR / settings.app.main_logo
        self.setWindowIcon(QIcon(str(logo_path)))

    def _setup_ui(self, event_stream: EventStream) -> None:
        self.menu_bar = Menu(self)
        self.setMenuBar(self.menu_bar)

        self.event_stream = event_stream

        self.event_widget = QPlainTextEdit(self)
        self.event_widget.setReadOnly(True)

        self.event_stream.attach(self.event_widget)
        self.setCentralWidget(self.event_widget)

        self.token_dialog = TokenDialog(self)

    def _connect_signals(self) -> None:
        self.menu_bar.start_requested.connect(self.start_requested.emit)
        self.menu_bar.stop_requested.connect(self.stop_requested.emit)
        self.menu_bar.restart_requested.connect(self.restart_requested.emit)

        self.menu_bar.token_requested.connect(self._show_token_dialog)
        self.menu_bar.exit_requested.connect(self.exit_requested.emit)
        self.token_dialog.token_accepted.connect(self.token_accepted.emit)

    def _show_token_dialog(self) -> None:
        self.token_dialog.exec()

    def set_running(self, running: bool) -> None:
        self.menu_bar.set_running(running)
