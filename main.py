# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets, uic

from src.controllers.controllers import Controller
from src.controllers.keyEventController import keyEventListener
from src.models.ApiModel import ApiModel
from src.views.views import mainWindows


class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = ApiModel()
        self.main_view = mainWindows()
        self.main_controller = Controller(self.main_view, self.model)

        self.main_view.show()


if __name__ == '__main__':
    KeyEventListener = keyEventListener()
    KeyEventListener.run()
    app = App(sys.argv)
    sys.exit(app.exec_())
