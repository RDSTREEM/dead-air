import math

from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import (
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QPen,
    QBrush,
    QColor,
    QFont,
    QWheelEvent,
)
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel


class Panel(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        self.setObjectName("Panel")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(10)

        self.title = QLabel(title.upper())
        self.title.setObjectName("PanelTitle")

        self.main_layout.addWidget(self.title)


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
            self._set_from_pos(event.position())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton:
            self._set_from_pos(event.position())

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        step = 0.1 if delta > 0 else -0.1
        self.set_freq(round(self.freq + step, 3))

    def paintEvent(self, event: QPaintEvent) -> None:  # i miss flutter auto compelete
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )  # im not sure if this one would look good with aliasing tho may change it to give a better radio feel
        side = min(self.width(), self.height())

        painter.translate(self.width() / 2, self.height() / 2)

        scale = side / 220
        painter.scale(scale, scale)

        # this is going to be horrible i tell u
        painter.setPen(QPen(QColor("#465247"), 3))
        painter.setBrush(QColor("#171D19"))
        painter.drawEllipse(QRectF(-100, -100, 200, 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#08100D"))
        painter.drawEllipse(QRectF(-88, -88, 176, 176))

        markings = 5  # very dumb name but like the marking per each thingi, u know how a ruler is

        for i in range(31):
            r = i / 30
            angle = math.radians(135 + r * 270)

            out = 83
            inner = 73 if i % markings == 0 else 78

            c = math.cos(angle)
            s = math.sin(angle)

            x1 = c * inner  # ?finally trig coming in handy???
            y1 = s * inner

            x2 = c * out
            y2 = s * out

            painter.setPen(
                QPen(QColor("#9D8891"), 1.8 if i % markings == 0 else 0.8)
            )  # writing in this pascal or camel whatever it is called case in python is really annoying
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        angle = math.radians(135 + self._ratio() * 270)
        painter.setPen(QPen(QColor("#D59A50"), 2.5))
        painter.drawLine(
            QPointF(0, 0), QPointF(math.cos(angle) * 67, math.sin(angle) * 67)
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#D59A50"))
        painter.drawEllipse(QRectF(-5, -5, 10, 10))

        painter.setPen(QColor("#9D8891"))

        font = QFont("Consolas", 10)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(
            QRectF(-65, 28, 130, 25),
            Qt.AlignmentFlag.AlignCenter,
            f"{self.freq:.3f}",
        )

        painter.setPen(QColor("#657A61"))
        painter.setFont(QFont("Consolas", 7))

        painter.drawText(
            QRectF(-65, 48, 130, 15),
            Qt.AlignmentFlag.AlignCenter,
            "MHz",
        )
