from PyQt5.QtWidgets import QDialog, QFontComboBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from utils import resource_path

class FontDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(resource_path("UI","Font_change.ui"), self)
        self.setWindowTitle("Choose Font")
        self.setWindowIcon(QIcon(resource_path("Logo.png")))

        self.parent = parent

        self.font_box = self.findChild(QFontComboBox, "Font_Box")

        if self.font_box is None:
            print("ERROR: Font_box not found in Font_change.ui")
            return

        current_font = self.parent.textEdit.currentFont()
        self.font_box.setCurrentFont(current_font)

        self.font_box.currentFontChanged.connect(self.apply_font)

    def apply_font(self, font):
        self.parent.textEdit.setCurrentFont(font)