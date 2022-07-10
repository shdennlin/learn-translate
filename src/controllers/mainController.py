from PySide6.QtCore import QEvent
from src.models.ApiModel import ApiModel
from src.views.views import MainWindow, SettingWindow


class MainController():
    def __init__(self, main_window, setting_window):
        super(MainController, self).__init__()
        self._main_window: MainWindow = main_window
        self._settingWindows: SettingWindow = setting_window
        self._model: ApiModel = ApiModel()

        # Define object and event
        self._main_window.translate_button.clicked.connect(self.translate_event)
        self._main_window.setting_button.clicked.connect(self.openSettingWindows)

    def translate_event(self):
        text = self._main_window.input_content.toPlainText()
        self._model.query(text)

        self._main_window.output_content.setPlainText("")
        self._main_window.output_content.appendHtml(self._model.res_html_en)
        self._main_window.output_content.appendHtml(self._model.res_html_zh)

    def openSettingWindows(self):
        self._settingWindows.ui.show()
