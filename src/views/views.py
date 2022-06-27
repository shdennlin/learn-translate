from tkinter import W
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
import sys

class mainWindows(QtWidgets.QWidget):
    def __init__(self):
        super(mainWindows, self).__init__()
        uic.loadUi('src/views/main_windows.ui', self)



class settingWindows(QtWidgets.QDialog):
    def __init__(self):
        super(settingWindows, self).__init__()
        uic.loadUi('src/views/setting_windows.ui', self)