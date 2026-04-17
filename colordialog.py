from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtGui import QIcon
from utils import resource_path

class ColorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(resource_path("UI", "color_picker.ui"), self)

        self.setWindowTitle("Choose Color")
        self.setWindowIcon(QIcon(resource_path("Logo.png")))
        self.parent = parent

        self.RedSlider.valueChanged.connect(self.update_color)
        self.GreenSlider.valueChanged.connect(self.update_color)
        self.BlueSlider.valueChanged.connect(self.update_color)

        self.HexCodeLine.textChanged.connect(self.hex_changed)
        self.btnApply.clicked.connect(self.apply_color)

        self.update_color()

    def update_color(self):
        r = self.RedSlider.value()
        g = self.GreenSlider.value()
        b = self.BlueSlider.value()

        self.RedValue.setText(str(r))
        self.GreenValue.setText(str(g))
        self.BlueValue.setText(str(b))

        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        self.HexCodeLine.blockSignals(True)
        self.HexCodeLine.setText(hex_color)
        self.HexCodeLine.blockSignals(False)

        self.update_preview(r, g, b)

    def hex_changed(self):
        text = self.HexCodeLine.text().strip()

        if not text.startswith("#"):
            text = "#" + text

        color = QColor(text)

        if color.isValid():
            self.RedSlider.blockSignals(True)
            self.GreenSlider.blockSignals(True)
            self.BlueSlider.blockSignals(True)

            self.RedSlider.setValue(color.red())
            self.GreenSlider.setValue(color.green())
            self.BlueSlider.setValue(color.blue())

            self.RedSlider.blockSignals(False)
            self.GreenSlider.blockSignals(False)
            self.BlueSlider.blockSignals(False)

            self.update_preview(color.red(), color.green(), color.blue())

    def update_preview(self, r, g, b):
        self.Preview.setStyleSheet(f"""
            background-color: rgb({r}, {g}, {b});
            border: 2px solid white;
            border-radius: 10px;
        """)

    def apply_color(self):
        r = self.RedSlider.value()
        g = self.GreenSlider.value()
        b = self.BlueSlider.value()

        color = QColor(r, g, b)

        cursor = self.parent.textEdit.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(color)

        cursor.mergeCharFormat(fmt)
        self.parent.textEdit.setTextCursor(cursor)

        self.close()