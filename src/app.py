import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtCore import Qt
from ui import MainWindow, resource_path


def main():
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    app.setWindowIcon(QIcon(resource_path("img", "icon.ico")))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, Qt.white)

    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()