import sys

from PySide6.QtWidgets import QApplication

from dead_air.app.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("DEAD AIR")
    app.setOrganizationName("Blackwater")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
