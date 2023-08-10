import sys
from mainwindow import MousePositionWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MousePositionWindow()
    window.show()
    sys.exit(app.exec())

