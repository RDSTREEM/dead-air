import math

import numpy as np
import soundfile as sf

from scipy.signal import spectrogram

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
    QImage,
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

    MIN_FREQUENCY = 0.5
    MAX_FREQUENCY = 108.0

    START_ANGLE = 135.0
    SWEEP_ANGLE = 270.0

    def __init__(self, parent=None):
        super().__init__(parent)

        self.freq = 91.400
        self._dragging = False

        self.setMinimumSize(180, 180)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    @property
    def frequency(self):
        return self.freq

    def _ratio(self):
        return (self.freq - self.MIN_FREQUENCY) / (
            self.MAX_FREQUENCY - self.MIN_FREQUENCY
        )

    def set_freq(self, frequency: float):
        frequency = max(self.MIN_FREQUENCY, min(self.MAX_FREQUENCY, frequency))

        if abs(frequency - self.freq) < 0.000001:
            return

        self.freq = frequency
        self.update()
        self.changed.emit(self.freq)

    def _set_from_ratio(self, ratio: float):
        ratio = max(0.0, min(1.0, ratio))

        frequency = self.MIN_FREQUENCY + ratio * (
            self.MAX_FREQUENCY - self.MIN_FREQUENCY
        )

        self.set_freq(frequency)

    def _pointer_ratio(self, position):
        x = position.x() - self.width() / 2
        y = position.y() - self.height() / 2

        angle = math.degrees(math.atan2(y, x)) % 360

        # The dial has a 90-degree gap at the bottom.
        # Angles between 45 and 135 are clamped
        # to the nearest endpoint.
        if 45 < angle < 135:
            return 1.0 if angle < 90 else 0.0

        if angle >= 135:
            ratio = (angle - 135) / 270
        else:
            ratio = (angle + 225) / 270

        return max(0.0, min(1.0, ratio))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self.setFocus()

            self._set_from_ratio(self._pointer_ratio(event.position()))

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            self._set_from_ratio(self._pointer_ratio(event.position()))

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        steps = event.angleDelta().y() / 120

        self.set_freq(self.freq + steps * 0.001)

        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        side = min(self.width(), self.height())

        painter.translate(self.width() / 2, self.height() / 2)

        painter.scale(side / 220, side / 220)

        # Outer casing
        painter.setPen(QPen(QColor("#465247"), 3))
        painter.setBrush(QColor("#171D19"))

        painter.drawEllipse(QRectF(-100, -100, 200, 200))

        # Inner face
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#08100D"))

        painter.drawEllipse(QRectF(-88, -88, 176, 176))

        # Frequency markings
        for i in range(31):
            ratio = i / 30

            angle = math.radians(self.START_ANGLE + ratio * self.SWEEP_ANGLE)

            major = i % 5 == 0

            inner = 72 if major else 78
            outer = 83

            x1 = math.cos(angle) * inner
            y1 = math.sin(angle) * inner

            x2 = math.cos(angle) * outer
            y2 = math.sin(angle) * outer

            painter.setPen(QPen(QColor("#9DBB91"), 1.8 if major else 0.8))

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Needle
        angle = math.radians(self.START_ANGLE + self._ratio() * self.SWEEP_ANGLE)

        painter.setPen(QPen(QColor("#D59A50"), 2.5))

        painter.drawLine(
            QPointF(0, 0), QPointF(math.cos(angle) * 67, math.sin(angle) * 67)
        )

        # Needle centre
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#D59A50"))

        painter.drawEllipse(QRectF(-5, -5, 10, 10))

        # Frequency display
        painter.setPen(QColor("#9DBB91"))

        font = QFont("Consolas", 10)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(
            QRectF(-65, 28, 130, 25), Qt.AlignmentFlag.AlignCenter, f"{self.freq:.3f}"
        )

        painter.setPen(QColor("#657A61"))
        painter.setFont(QFont("Consolas", 7))

        painter.drawText(QRectF(-65, 48, 130, 15), Qt.AlignmentFlag.AlignCenter, "MHz")


class SignalMeter(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 0.0
        self.setMinimumHeight(25)

    def set_level(self, level: float):
        self.level = max(0.0, min(1.0, level))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        segments = 24
        gap = 3

        seg_width = self.width() - gap * (segments - 1) / segments

        active = int(self.level * segments)

        for i in range(segments):
            x = i * (seg_width + gap)

            if i < active:
                if i > 20:
                    c = QColor("#D59A50")
                else:
                    c = QColor("#9DBB91")

            else:
                c = QColor("#283328")

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(c)

            painter.drawRoundedRect(
                QRectF(
                    x,
                    3,
                    seg_width,
                    self.height() - 6,
                ),
                2,
                2,
            )
        painter.end()


class Analyzer(QWidget):
    # for now, will add actual forier [wow spelling] transform and stuff later

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.name = name
        self.image = None
        self.duration = 0
        self.max_freq = 5000  # i do wonder tho if i didnt know the max freq for the audio what i would set here
        self.setMinimumSize(300, 220)

    def load(self, path):
        # confusionnnnn on what i am doing but still
        print(path)
        audio, samp = sf.read(path)

        if audio.ndim == 2:  # if it is sterio to average em out i think
            audio = audio.mean(axis=1)

        freq, times, vals = spectrogram(
            audio,
            fs=samp,
            nperseg=1024,
            noverlap=512,
        )

        # from my understanding this converts it into decibals, if i was using the short tiem forier (spellinggg) transform i would have needed to do 20 * the log cuz it is not squared.
        e = 1e-10
        deci = 10 * np.log10(vals + e)
        deci = np.flipud(
            deci
        )  # because of how numpy processes arrays, we need to flip it to make 0 at the bottom

        min_val = deci.min()
        max_val = deci.max()

        # to make it into an image, the values must be normalized btn 0 and 255
        if max_val - min_val > 0:
            n = 255 * (deci - min_val) / (max_val - min_val)
        else:
            n = np.zeros_like(deci)

        img = n.astype(np.uint8)
        img = np.ascontiguousarray(img)

        h, w = img.shape
        image = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
        self.image = image.copy()
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor("#080D0A"))

        if self.image is None:
            painter.setPen(QColor("#657A61"))
            painter.setFont(QFont("Consolas", 10))
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, "No Signal Analysis Loaded"
            )
            painter.end()
            return

        l, t, r, b = 48, 15, 15, 32
        area = QRectF(l, t, self.width() - l - r, self.height() - t - b)
        painter.drawImage(area, self.image)

        painter.end()
