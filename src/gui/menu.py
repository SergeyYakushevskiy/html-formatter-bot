from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMenuBar, QMenu


class Menu(QMenuBar):
    start_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    restart_requested = pyqtSignal()
    token_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.bot_menu = QMenu("Бот", self)
        self.addMenu(self.bot_menu)

        self.run_action = self.bot_menu.addAction("Запустить")
        self.run_action.triggered.connect(self._toggle_bot)

        self.restart_action = self.bot_menu.addAction("Перезапустить")
        self.restart_action.triggered.connect(self.restart_requested.emit)

        self.bot_menu.addSeparator()

        self.token_action = self.bot_menu.addAction("Задать токен")
        self.token_action.triggered.connect(self.token_requested.emit)

        self.bot_menu.addSeparator()

        self.exit_action = self.bot_menu.addAction("Выход")
        self.exit_action.triggered.connect(self.exit_requested.emit)

        self._is_running = False

    def set_running(self, running: bool) -> None:
        self._is_running = running
        self.run_action.setText("Остановить" if running else "Запустить")

    def _toggle_bot(self) -> None:
        if self._is_running:
            self.stop_requested.emit()
        else:
            self.start_requested.emit()
