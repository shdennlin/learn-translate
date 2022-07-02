from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, pyqtSlot, Qt
from PyQt5 import QtWidgets
from src.models.ApiModel import ApiModel
from src.views.views import mainWindows, settingWindows


class Controller():
    def __init__(self, view, api_model):
        super(Controller, self).__init__()
        self._mainWindows = view
        self._settingWindows = settingWindows()
        self._model: ApiModel = api_model

        self.input_content = self._mainWindows.findChild(
            QtWidgets.QPlainTextEdit, 'input_content')
        self.output_content = self._mainWindows.findChild(
            QtWidgets.QPlainTextEdit, 'output_content')

        # Define object and event
        self._mainWindows.translate_button = self._mainWindows.findChild(
            QtWidgets.QPushButton, 'translate_button')
        self._mainWindows.translate_button.clicked.connect(
            self.translate_event)

        self._mainWindows.setting_button = self._mainWindows.findChild(
            QtWidgets.QPushButton, 'setting_button')
        self._mainWindows.setting_button.clicked.connect(
            self.openSettingWindows)

    def translate_event(self):
        text = self.input_content.toPlainText()
        self._model.query(text)
        # print(self._model.res)
        # res = self._model.res["translation"]

        self.output_content.setPlainText("")
        self.output_content.appendHtml(self._model.res_html_en)
        self.output_content.appendHtml(self._model.res_html_zh)

    def openSettingWindows(self):
        self._settingWindows.show()
