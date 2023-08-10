import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout
from PySide6.QtGui import Qt, QAction, QKeySequence
from PySide6.QtCore import QPointF
import pyautogui
from threading import Thread
import time

print(pyautogui.size())


class MousePositionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Posición del Ratón")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Q))
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

        screen_resolution = QApplication.primaryScreen().availableGeometry()
        self.setStyleSheet("QMainWindow{background-color: darkgray;"
                           "border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Establece la posición y el tamaño de la ventana
        self.setGeometry(screen_resolution.width() - 224, 0, 224, 50)
        print(screen_resolution)

        self.mouse_position_label = QLabel(self)
        self.mouse_position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mouse_position_label.setStyleSheet(
            "QLabel{background-color: rgb(0,0,0); border: 1px solid red;"
            " color: rgb(255,255,255); font: bold italic 20pt"
            " 'Times New Roman';}")

        self.mouse_position_label.setGeometry(0, 0, 224, 50)
        layout = QHBoxLayout()
        layout.addWidget(self.mouse_position_label)

        self.setLayout(layout)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.update_thread = Thread(target=self.update_mouse_position)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.old_pos = self.pos()
        self.show()

    def update_mouse_position(self):
        try:
            while True:
                x, y = pyautogui.position()
                position_str = f"x = {x}, y = {y}"
                self.mouse_position_label.setText(position_str)
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        delta = QPointF(event.globalPosition() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MousePositionWindow()
    window.show()
    sys.exit(app.exec())

