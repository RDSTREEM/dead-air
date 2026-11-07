from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QTabWidget,
    QListWidget,
    QPushButton,
    QTextEdit,
    QDoubleSpinBox,
    QSlider,
)

from dead_air.app.widgets import Panel, FrequencyDial, Analyzer, SignalMeter
from dead_air.engine.signal_catalogue import SignalCatalogue
from dead_air.engine.receiver import Receiver


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

        catalogue = (
            Path(__file__).resolve().parents[1] / "data" / "signals.json"
        )  # ? im not sure if i should have this in the actual app or as a separate folder cuz i dont want people to be snoopin
        self.receiver = Receiver(SignalCatalogue.load(catalogue))

        self.audio_dir = Path(__file__).resolve().parents[1] / "assets" / "audio"
        self.audio_output = QAudioOutput(self)
        self.audio_output.setVolume(0.7)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)

        self.current_audio = None
        self.setup_ui()

    def setup_ui(self):
        c = QWidget()
        self.setCentralWidget(c)

        layout = QVBoxLayout(c)
        layout.setContentsMargins(12, 12, 12, 8)
        layout.setSpacing(10)
        # layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.create_header())

        workstation = QHBoxLayout()
        workstation.setSpacing(10)

        workstation.addWidget(self.create_receiver(), 0)
        workstation.addWidget(self.create_analyzer(), 1)
        workstation.addWidget(self.create_archive(), 0)

        layout.addLayout(workstation, 1)

        layout.addWidget(self.create_status_bar())

        self.freq_input.valueChanged.connect(self.on_freq_change)
        self.on_freq_change(self.freq_input.value())

    def create_receiver(self):
        panel = Panel("01 / RECEIVER")
        panel.setMaximumWidth(260)
        panel.setMinimumWidth(290)

        d_cont = QHBoxLayout()

        self.freq = FrequencyDial()

        d_cont.addStretch()
        d_cont.addWidget(self.freq)
        d_cont.addStretch

        panel.main_layout.addLayout(d_cont)

        label = QLabel("TUNING FREQUENCY")

        self.freq_input = QDoubleSpinBox()
        self.freq_input.setRange(0.6, 108.0)
        self.freq_input.setDecimals(3)
        self.freq_input.setSingleStep(0.001)
        self.freq_input.setSuffix("MHz")
        self.freq_input.setValue(91.4)

        self.freq_input.setObjectName("FrequencyDisplay")

        self.freq.changed.connect(self.freq_input.setValue)

        self.freq_input.valueChanged.connect(self.freq.set_freq)

        panel.main_layout.addWidget(label)
        panel.main_layout.addWidget(self.freq_input)

        fine_tune = QHBoxLayout()
        decrease = QPushButton(" - 0.001 ")
        increase = QPushButton(" + 0.001 ")

        decrease.clicked.connect(
            lambda: self.freq_input.setValue(self.freq_input.value() - 0.001)
        )
        increase.clicked.connect(
            lambda: self.freq_input.setValue(self.freq_input.value() + 0.001)
        )

        fine_tune.addWidget(decrease)
        fine_tune.addWidget(increase)

        panel.main_layout.addLayout(fine_tune)
        panel.main_layout.addSpacing(12)

        title = QLabel("SIGNAL STRENGTH")

        self.signal_meter = SignalMeter()
        self.signal_val = QLabel("NO SIGNAL")
        self.signal_val.setObjectName("Muted")

        panel.main_layout.addWidget(title)
        panel.main_layout.addWidget(self.signal_meter)
        panel.main_layout.addWidget(self.signal_val)

        panel.main_layout.addSpacing(10)
        transport_title = QLabel("TRANSPORT")
        transport = QHBoxLayout()
        self.rec = QPushButton("REC")
        self.play = QPushButton("PLAY")
        self.stop = QPushButton("STOP")
        self.play.clicked.connect(self.player.play)
        self.stop.clicked.connect(self.player.stop)
        self.rec.setEnabled(False)

        transport.addWidget(self.rec)
        transport.addWidget(self.play)
        transport.addWidget(self.stop)

        panel.main_layout.addWidget(transport_title)
        panel.main_layout.addLayout(transport)

        v_layout = QHBoxLayout()
        v_label = QLabel("VOLUME")

        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(70)

        self.volume.valueChanged.connect(
            lambda val: self.audio_output.setVolume(val / 100)
        )

        v_layout.addWidget(v_label)
        v_layout.addWidget(self.volume)

        panel.main_layout.addSpacing(10)
        panel.main_layout.addLayout(v_layout)

        engine = QLabel("AUDIO ENGINE: ONLINE")
        engine.setObjectName("Muted")

        panel.main_layout.addStretch()
        panel.main_layout.addWidget(engine)

        return panel

    def create_header(self):
        header = QFrame()
        header.setObjectName("Panel")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 10, 15, 10)

        identity = QVBoxLayout()

        title = QLabel("DEAD AIR")
        title.setObjectName("HeaderTitle")

        subtitle = QLabel("BLACKWATER COASTAL RADIO STATION")
        subtitle.setObjectName("HeaderSubtitle")
        identity.addWidget(title)
        identity.addWidget(subtitle)

        layout.addLayout(identity)

        layout.addStretch()

        station = QLabel("Station: BCR-17")
        station.setObjectName("StatusValue")

        system = QLabel(
            "ARCHIVE SYSTEM: ONLINE"
        )  # since the puzzles starts as an archival thingi
        system.setObjectName("StatusValue")

        layout.addWidget(station)
        layout.addSpacing(25)
        layout.addWidget(system)

        return header

    def create_analyzer(self):
        panel = Panel("02 / Signal Analyzer")

        self.analyzer_tabs = QTabWidget()
        self.waveform = Analyzer("Waveform")
        self.spectogram = Analyzer("Spectogram")
        self.analyzer_tabs.addTab(self.waveform, "WAVEFORM")
        self.analyzer_tabs.addTab(self.spectogram, "SPECTOGRAM")

        panel.main_layout.addWidget(self.analyzer_tabs, 1)

        info = QLabel(
            "NO RECORDING LOADED" "        |    SAMPLE RATE: " "        |    DURATION: "
        )
        info.setObjectName("Muted")
        panel.main_layout.addWidget(info)
        return panel

    def create_archive(self):
        panel = Panel("03 / Archive")
        panel.setMinimumWidth(260)
        panel.setMaximumWidth(310)

        self.archive_tabs = QTabWidget()

        archive = QWidget()
        a_layout = QVBoxLayout(archive)

        desc = QLabel("AVIALABLE RECORDINGS AND DOCUMENTS")
        desc.setObjectName("Muted")

        self.list = QListWidget()
        self.list.addItems(
            [
                "weather_01.wav",
                "empty_channel.wav",
                "frequency_allocation_register",
                "analyzer_manual",
            ]
        )

        a_layout.addWidget(desc)
        a_layout.addWidget(self.list)

        open_btn = QPushButton("OPEN SELECTED")
        open_btn.setEnabled(False)

        a_layout.addWidget(open_btn)

        logbook = QWidget()
        l_layout = QVBoxLayout(logbook)

        l_desc = QLabel("INVESTIGATION NOTES")
        l_desc.setObjectName("Muted")

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("No discoveries recorded.")

        l_layout.addWidget(l_desc)
        l_layout.addWidget(self.log)

        self.archive_tabs.addTab(archive, "ARCHIVE")
        self.archive_tabs.addTab(logbook, "LOGBOOK")

        panel.main_layout.addWidget(self.archive_tabs, 1)

        return panel

    def create_status_bar(self):
        bar = QFrame()
        bar.setObjectName("Panel")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 6, 12, 6)

        self.status_msg = QLabel("SYSTEM // AWAITING OPERATOR INPUT")
        self.status_msg.setObjectName("Muted")

        right = QLabel("BCR-17  |   ARCHIVE TERMINAL 01")
        right.setObjectName("Muted")
        layout.addWidget(self.status_msg)
        layout.addStretch()
        layout.addWidget(right)

        return bar

    def on_freq_change(self, freq: float):
        reception = self.receiver.tune(freq)
        self.signal_meter.set_level(reception.strength)

        if reception.signal is None:
            audio_file = self.audio_dir / "static_loop.wav"
            self.signal_val.setText("NO KNOWN CARRIER")
            self.signal_val.setStyleSheet("color: #657A61;")
            self.status_msg.setText("RECEIVER // NO IDENTIFIED TRANSMISSION")
        else:
            audio_file = self.audio_dir / reception.signal.audio_file
            signal = reception.signal
            self.signal_val.setText(signal.name.upper())
            self.signal_val.setStyleSheet("color: #9DBB91;")
            self.status_msg.setText(f"CARRIER DETECTED // {signal.id.upper()}")

        p = str(audio_file.resolve())

        if p != self.current_audio and audio_file.exists():
            self.player.stop()
            self.player.setSource(QUrl.fromLocalFile(p))
            self.player.play()
            self.current_audio = p
