import os
import time
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from utils import resource_path

def show_file_info(parent, text, file_path=None):
    chars = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    spaces = text.count(" ")

    if file_path and os.path.exists(file_path):
        size = os.path.getsize(file_path)
        created = time.ctime(os.path.getctime(file_path))
        modified = time.ctime(os.path.getmtime(file_path))
        file_type = os.path.splitext(file_path)[1] or "Unknown"
    else:
        file_path = "Unsaved File"
        size = 0
        created = "N/A"
        modified = "N/A"
        file_type = "Unknown"

    dialog = QDialog(parent)
    dialog.setWindowTitle("File Information")
    dialog.resize(420, 300)
    dialog.setWindowIcon(QIcon(resource_path("Logo.png")))

    # 🔥 THEME
    dialog.setStyleSheet("""
    QDialog {
        background-color: #181b28;
        color: white;
    }

    QLabel {
        color: white;
        font-family: Consolas;
        font-size: 12px;
    }
    """)

    layout = QVBoxLayout()

    info = f"""
File: {file_path}
Type: {file_type}
Size: {size} bytes

Created: {created}
Modified: {modified}

------------------------
Characters: {chars}
Words: {words}
Lines: {lines}
Spaces: {spaces}
------------------------
"""

    label = QLabel(info)
    label.setTextInteractionFlags(Qt.TextSelectableByMouse)

    layout.addWidget(label)
    dialog.setLayout(layout)

    dialog.exec_()