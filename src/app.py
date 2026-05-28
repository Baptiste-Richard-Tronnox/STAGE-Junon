import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QPainter, QFont
from PySide6.QtCore import Qt, QTimer
from ui import MainWindow, resource_path


class SplashScreen(QSplashScreen):
    def __init__(self):
        # Crée un pixmap de fond aux couleurs de l'app
        pixmap = QPixmap(480, 280)
        pixmap.fill(QColor(30, 30, 46))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Icône centrée
        icon = QPixmap(resource_path("img", "icon.ico"))
        if not icon.isNull():
            icon = icon.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (480 - icon.width()) // 2
            painter.drawPixmap(x, 60, icon)

        # Titre
        painter.setPen(QColor(205, 214, 244))  # #cdd6f4
        font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect().adjusted(0, 150, 0, 0), Qt.AlignHCenter, "Dataminapp")

        # Sous-titre
        painter.setPen(QColor(166, 173, 200))  # #a6adc8
        font2 = QFont("Segoe UI", 10)
        painter.setFont(font2)
        painter.drawText(pixmap.rect().adjusted(0, 190, 0, 0), Qt.AlignHCenter, "Chargement en cours...")

        painter.end()

        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(resource_path("img", "icon.ico")))

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    # Affiche le splash
    splash = SplashScreen()
    splash.show()
    app.processEvents()  # Force l'affichage immédiat

    # Charge la MainWindow
    window = MainWindow()

    # Ferme le splash et affiche la fenêtre principale
    splash.finish(window)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()