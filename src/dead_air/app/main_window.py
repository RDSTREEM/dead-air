from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DEAD AIR")
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)

        self.setup_ui()

    def setup_ui(self):
        c = QWidget()
        self.setCentralWidget(c)

        layout = QVBoxLayout(c)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("DEAD AIR")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(title)
