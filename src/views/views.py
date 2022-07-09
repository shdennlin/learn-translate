import sys

from loguru import logger
from PySide6 import QtUiTools
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import (QCheckBox, QDialog, QLabel, QLineEdit,
                               QMainWindow, QPlainTextEdit, QPushButton,
                               QWidget)


def load_ui_file(file_path):
    ui_file = QFile(file_path)
    if not ui_file.open(QIODevice.ReadOnly):
        ui_file.close()
        logger.error(f"Cannot open {file_path}: {ui_file.errorString()}")
        sys.exit(-1)
    ui = QtUiTools.QUiLoader().load(ui_file, None)
    return ui


class mainWindows(QWidget):
    def __init__(self):
        super(mainWindows, self).__init__()
        self.ui = load_ui_file("src/views/main_windows.ui")

        self.input_content = self.ui.findChild(QPlainTextEdit, 'input_content')
        self.output_content = self.ui.findChild(QPlainTextEdit, 'output_content')
        self.translate_button = self.ui.findChild(QPushButton, 'translate_button')
        self.setting_button = self.ui.findChild(QPushButton, 'setting_button')


class settingWindows(QDialog):
    def __init__(self):
        super(settingWindows, self).__init__()
        self.ui = load_ui_file("src/views/setting_windows.ui")
