# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from src.controllers.mainController import MainController
from src.controllers.hokeyController import HokeyController
from src.views.views import MainWindow, SettingWindow


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # define windows
        self.main_window = MainWindow()
        self.setting_window = SettingWindow()

        # define controllers
        self.main_controller = MainController(self.main_window, self.setting_window)
        self.hokey_controller = HokeyController(self.main_window)

        # self.hokey_controller.run()

        self.main_window.ui.show()
        # self.main_window.input_content.setFocus()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
