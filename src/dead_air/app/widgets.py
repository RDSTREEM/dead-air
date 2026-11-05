import math

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
    QFont,
)
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel


class Panel(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.setObjectName("Panel")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(12, 12, 12, 12)
        self._layout.setSpacing(10)

        self.title = QLabel(title.upper())
        self.title.setObjectName("PanelTitle")

        self._layout.addWidget(self.title)
