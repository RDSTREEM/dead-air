from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)

from dead_air.app.widgets import Panel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DEAD AIR")
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #101311;
            }
            
            QWidget {
                color: #88C885;
                font-family: Consolas;
            }
            
            QLabel {
                color: #88C885;
            }
            """)

        self.setup_ui()

    def setup_ui(self):
        c = QWidget()
        self.setCentralWidget(c)

        layout = QVBoxLayout(c)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("DEAD AIR")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #9DBB91;
            letter-spacing: 5px;
            """)

        subtitle = QLabel("BLACKWATER COASTAL RADIO STATION")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 11px;
            color: #657A61;
            letter-spacing: 3px;
            """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.create_reciever())

    def create_reciever(self):
        panel = Panel("01/ Reciever")
        panel.setMaximumWidth(260)
        panel.setMinimumWidth(290)

        return panel
