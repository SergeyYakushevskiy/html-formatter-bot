from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)


class TokenDialog(QDialog):
    token_accepted = pyqtSignal(str)
    cancelled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Токен бота")
        self.setModal(True)

        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        label = QLabel(
            "Введите токен бота в формате:\n"
            "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789"
        )
        layout.addWidget(label)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Токен бота")
        layout.addWidget(self.token_input)

        buttons_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Отмена")
        self.accept_button = QPushButton("Принять")

        buttons_layout.addWidget(self.accept_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.accept_button.clicked.connect(self._accept)
        self.cancel_button.clicked.connect(self._cancel)

        self.accept_button.setDefault(True)
        self.cancel_button.setAutoDefault(False)

    def _accept(self) -> None:
        token = self.token_input.text().strip()

        self.token_accepted.emit(token)
        self.accept()

    def _cancel(self) -> None:
        self.cancelled.emit()
        self.reject()
