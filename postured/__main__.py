import sys
from PyQt6.QtWidgets import QApplication
from .app import Application


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running with just tray icon

    postured = Application()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
