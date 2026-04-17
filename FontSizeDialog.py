from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from utils import resource_path

class FontSizeDialog(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(resource_path("UI", "Font_size.ui"), self)
        self.setWindowTitle("Choose Font Size")
        self.setWindowIcon(QIcon(resource_path("Logo.png")))
        self.parent = parent

        self.Font_Size_Box.setValue(
            self.parent.textEdit.font().pointSize()
        )

        self.Font_Size_Box.valueChanged.connect(self.apply_size)

    def apply_size(self):
        size = self.Font_Size_Box.value()

        font = self.parent.textEdit.currentFont()
        font.setPointSize(size)

        self.parent.textEdit.setCurrentFont(font)