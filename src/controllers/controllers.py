from PySide6.QtWidgets import (QCheckBox, QDialog, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QWidget, QPlainTextEdit)
from src.models.ApiModel import ApiModel
from src.views.views import mainWindows, settingWindows


class Controller():
    def __init__(self, view):
        super(Controller, self).__init__()
        self._mainWindows = view
        self._settingWindows = settingWindows()
        self._model: ApiModel = ApiModel()

        # Define object and event
        self._mainWindows.translate_button.clicked.connect(self.translate_event)
        self._mainWindows.setting_button.clicked.connect(self.openSettingWindows)

    def translate_event(self):
        text = self._mainWindows.input_content.toPlainText()
        self._model.query(text)

        self._mainWindows.output_content.setPlainText("")
        self._mainWindows.output_content.appendHtml(self._model.res_html_en)
        self._mainWindows.output_content.appendHtml(self._model.res_html_zh)

    def openSettingWindows(self):
        self._settingWindows.ui.show()
