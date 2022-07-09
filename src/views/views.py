import sys

from loguru import logger
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, QEvent
from PySide6.QtWidgets import (QDialog, QPlainTextEdit, QPushButton, QWidget)


def load_ui_file(file_path) -> QUiLoader:
    ui_file = QFile(file_path)
    if not ui_file.open(QIODevice.ReadOnly):
        ui_file.close()
        logger.error(f"Cannot open {file_path}: {ui_file.errorString()}")
        sys.exit(-1)
    ui = QUiLoader().load(ui_file, None)
    return ui


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui: QUiLoader = load_ui_file("src/views/main_windows.ui")

        self.input_content = self.ui.findChild(QPlainTextEdit, 'input_content')
        self.output_content = self.ui.findChild(QPlainTextEdit, 'output_content')
        self.translate_button = self.ui.findChild(QPushButton, 'translate_button')
        self.setting_button = self.ui.findChild(QPushButton, 'setting_button')

class SettingWindow(QDialog):
    def __init__(self):
        super(SettingWindow, self).__init__()
        self.ui = load_ui_file("src/views/setting_windows.ui")
