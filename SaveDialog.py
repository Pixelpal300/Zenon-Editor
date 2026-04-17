from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from utils import resource_path
import sys

class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(resource_path("UI", "popup.ui"), self)

        self.setWindowIcon(QIcon(resource_path("Logo.png")))
        self.setWindowTitle("Save Changes?")
        self.pushButton.clicked.connect(self.save_clicked)  
        self.pushButton_2.clicked.connect(self.dont_save)      
        self.pushButton_3.clicked.connect(self.cancel_clicked) 
        self.choice = None

    def save_clicked(self):
        self.choice = "Save"
        self.accept()

    def dont_save(self):
        self.choice = "Don't Save"
        self.accept()

    def cancel_clicked(self):
        self.choice = "cancel"
        sys.exit()
        self.reject()