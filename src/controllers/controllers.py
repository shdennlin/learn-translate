from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5 import QtWidgets

class Controller(QObject):
    def __init__(self, view, model):
        super().__init__()
        self.ui = view
        self._model = model

        
        self.input_content = self.ui.findChild(QtWidgets.QPlainTextEdit, 'input_content')
        self.output_content = self.ui.findChild(QtWidgets.QPlainTextEdit, 'output_content')

        # Define object and event
        self.ui.translate_button = self.ui.findChild(QtWidgets.QPushButton, 'translate_button')
        self.ui.translate_button.clicked.connect(self.translate_event)
    
    @pyqtSlot()
    def translate_event(self):
        text = self.input_content.toPlainText()
        self.output_content.setPlainText(text)
        print(text)