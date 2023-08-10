from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout
from PySide6.QtGui import Qt, QAction, QKeySequence
from PySide6.QtCore import QPointF
import pyautogui
from threading import Thread
import time


class MousePositionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse Position")
        
        #Sets the exit shortcut
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Q))
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)

        #Style the window.
        self.setStyleSheet("QMainWindow{background-color: darkgray;"
                           "border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Establishes the window in the top right corner
        screen_resolution = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_resolution.width() - 224, 0, 224, 50)

        #Style the label
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
        
        #Overlay any other window
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        #Starts the updating thread
        self.update_thread = Thread(target=self.update_mouse_position)
        self.update_thread.daemon = True
        self.update_thread.start()

        #Gets the window position
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
        #Allows the window to be draggable
        delta = QPointF(event.globalPosition() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition()
