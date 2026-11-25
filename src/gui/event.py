import logging

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPlainTextEdit


class EventStream(QObject):
    text_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.text_received.connect(self._append_text)
        self.widget: QPlainTextEdit | None = None
        self.buffer: list[str] = []

    def attach(self, widget: QPlainTextEdit) -> None:
        self.widget = widget
        self.widget.setReadOnly(True)
        self.widget.setMaximumBlockCount(1000)
        self.widget.setFont(QFont("Monospace", 10))

        if self.buffer:
            self.widget.insertPlainText("".join(self.buffer))
            self.buffer.clear()

    def write(self, text: str) -> int:
        if self.widget is None:
            self.buffer.append(text)
        else:
            self.text_received.emit(text)

        return len(text)

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    @property
    def encoding(self) -> str:
        return "utf-8"

    @pyqtSlot(str)
    def _append_text(self, text: str) -> None:
        if self.widget is None:
            return

        self.widget.moveCursor(self.widget.textCursor().MoveOperation.End)
        self.widget.insertPlainText(text)
        self.widget.ensureCursorVisible()
