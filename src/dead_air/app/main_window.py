from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

from dead_air.app.widgets import Panel, FrequencyDial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DEAD AIR")
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #101311;
                color: #88C885;
                font-family: Consolas;
                font-size: 11px;
            }
            
            QFrame#Panel {
                background-color: #171D19;
                border: 1px solid #303C32;
                border-radius: 4px;
            }
            
            QLabel#PanelTitle { 
                color: #9DBB91;
                font-size: 11px;
                font-weight: bld;
                letter-spacing: 2px;
                padding-bottom: 7px;
                border-bottom: 1px solid #303C32;
            }
            
            QLabel#Muted {
                color: #657A61;
            }
            
            QLabel#HeaderTitle {
                color: #A9C598;
                font-size: 20px;
                font-weight: bold;
                letter-spacing: 4px;
            }
            
            QLabel#HeaderSubtitle {
                color: #657A61;
                font-size: 9px;
                letter-spacing: 2px;
            }
            
            QLabel#FrequencyDisplay {
                color: #D59A50;
                font-size: 20px;
                font-weight: bold;
            }
            
            QLabel#StatusValue {
                color: #9DBB91;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #202A22;
                border: 1px solid #465247;
                border-radius: 3px;
                padding: 8px 12px;
                color: #B8C8B5;
            }
            
            QPushButton:hover {
                background-color: #2C392D;
                border-color: #9DBB91;
            }
            
            QPushButton:disabled {
                color: #536052;
                background-color: #171D19;
                border-color: #303C32;
            }

            QDoubleSpinBox {
                background-color: #080D0A;
                border: 1px solid #465247;
                padding: 6px;
                color: #D59A50;
                font-size: 14px;
            }

            QSlider::groove:horizontal {
                height: 5px;
                background: #303C32;
            }

            QSlider::handle:horizontal {
                background: #9DBB91;
                width: 12px;
                margin: -5px 0;
                border-radius: 3px;
            }

            QTabWidget::pane {
                border: 1px solid #303C32;
                background: #080D0A;
            }

            QTabBar::tab {
                background: #171D19;
                color: #657A61;
                padding: 9px 15px;
                border: 1px solid #303C32;
            }

            QTabBar::tab:selected {
                background: #253027;
                color: #A9C59B;
            }

            QListWidget, QTextEdit {
                background-color: #080D0A;
                border: 1px solid #303C32;
                color: #A9BBA5;
                padding: 5px;
            }

            QListWidget::item {
                padding: 7px;
            }

            QListWidget::item:selected {
                background-color: #304031;
                color: #D4E0CF;
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

        d_cont = QHBoxLayout()

        self.freq = FrequencyDial()

        d_cont.addStretch()
        d_cont.addWidget(self.freq)
        d_cont.addStretch

        panel.main_layout.addLayout(d_cont)

        return panel
