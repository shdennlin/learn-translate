from tkinter import W
from PyQt5 import uic, QtWidgets
import sys

class mainUI(QtWidgets.QWidget):
    def __init__(self):
        super(mainUI, self).__init__()
        uic.loadUi('src/views/main.ui', self)