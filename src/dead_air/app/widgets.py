import math

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import (
    QMouseEvent,
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


class FrequencyDial(QWidget):
    changed = Signal(float)

    def __init__(self, minimum=0.5, maximum=108.0, parent=None):
        super().__init__(parent)

        self.mini = minimum
        self.maxi = maximum
        self.freq = 91.4  # so would have loved to document all this in a google doc like i did for project ayk buttt since it gotta be code, this is going to be the starting freq for now

        self.setMinimumSize(190, 190)
        self.setMaximumSize(260, 260)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_freq(self, freq: float):
        freq = max(self.mini, min(self.maxi, freq))

        if abs(freq - self.freq) < 0.0001:
            return  # no point in changing if it is a small change plus to be radio like i want it to be 4 digit accurate

        self.freq = freq
        self.update()
        self.changed.emit(self.freq)

    def _ratio(self):
        return (self.freq - self.mini) / (self.maxi - self.freq)

    def _set_from_pos(self, pos: QPointF):
        center = QPointF(
            self.width() / 2, self.height() / 2
        )  # just remembered qt uses functions for width and height, whyyy

        dx = pos.x() - center.x()
        dy = pos.y() - center.y()

        angle = math.degrees(math.atan2(dy, dx))

        if angle < 135:
            angle += 360

        angle = max(135, min(405, angle))

        ratio = (angle - 135) / 270

        freq = self.mini + ratio * (self.maxi - self.mini)

        self.set_freq(round(freq, 3))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
