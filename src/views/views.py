import sys

if sys.platform == "win32":
    import win32gui
    import win32com.client as win32com_client

import time

from loguru import logger
from pynput import keyboard
from PySide6.QtCore import QEvent, QFile, QIODevice, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QPlainTextEdit, QPushButton, QWidget


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
        super(MainWindow, self).__init__(parent=None)
        if sys.platform == "win32":
            self.shell = win32com_client.Dispatch("WScript.Shell")
        self.ui: QUiLoader.load() = load_ui_file("src/views/main_windows.ui")
        self.ui.setFocusPolicy(Qt.StrongFocus)
        self.input_content = self.ui.findChild(QPlainTextEdit, 'input_content')
        self.output_content = self.ui.findChild(QPlainTextEdit, 'output_content')
        self.translate_button = self.ui.findChild(QPushButton, 'translate_button')
        self.setting_button = self.ui.findChild(QPushButton, 'setting_button')

        self.ui.installEventFilter(self)
        self.run()

    def run(self):
        def main_window_show():
            self.ui.show()

        def for_canonical(f):
            return lambda k: f(l.canonical(k))

        hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+y'), main_window_show)
        l = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
        )
        l.start()

    def eventFilter(self, widget, event) -> QWidget.eventFilter:
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Escape:
                self.ui.hide()
            elif key == Qt.Key_F3:
                self.translate_button.click()

        #　TODO Check windows is activate in Linux
        if event.type() == QEvent.ShowToParent:
            self.ui.setFocus()
            if sys.platform == "win32":
                self.shell.SendKeys('%')
                win32gui.SetForegroundWindow(win32gui.FindWindow(None, "Learn-translate"))
            self.ui.activateWindow()
            self.input_content.setFocus()

            if self.ui.isActiveWindow():
                self.input_content.setFocus()

        return QWidget.eventFilter(self, widget, event)


class SettingWindow(QDialog):
    def __init__(self):
        super(SettingWindow, self).__init__()
        self.ui = load_ui_file("src/views/setting_windows.ui")
