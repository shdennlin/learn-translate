# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from src.controllers.controllers import Controller
from src.controllers.keyEventController import keyEventListener
from src.views.views import mainWindows


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = mainWindows()
        self.main_controller = Controller(self.main_view)

        self.main_view.ui.show()


if __name__ == '__main__':
    # KeyEventListener = keyEventListener()
    # KeyEventListener.run()
    app = App(sys.argv)
    sys.exit(app.exec())
