
from pynput import keyboard
from PySide6.QtCore import QEvent, QFile, QIODevice, Qt
from PySide6.QtWidgets import QWidget


# TODO Move shortcut from views.py to here
# TODO Keyboard Shortcut Assignment https://www.youtube.com/watch?v=xnTPZ5fHvCc
class HokeyController():
    def __init__(self, mainWindow: QWidget):
        self._main_window = mainWindow
