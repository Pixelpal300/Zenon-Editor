from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from utils import resource_path
import os


class PluginDialog(QDialog):
    def __init__(self, plugin_manager):
        super().__init__()

        self.pm = plugin_manager

        self.setWindowTitle("Plugin Manager")
        self.setWindowIcon(QIcon(resource_path("Logo.png")))
        self.resize(450, 350)

        self.setStyleSheet("""
        QDialog {
            background-color: #181b28;
            color: white;
        }

        QListWidget {
            background-color: #181b28;
            color: white;
            border: 1px solid #2a2f45;
        }

        QPushButton {
            background-color: #181b28;
            color: white;
            border: 1px solid #2a2f45;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #2a2f45;
        }
        """)

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.toggle_btn = QPushButton("Enable / Disable")
        self.layout.addWidget(self.toggle_btn)

        self.load_btn = QPushButton("Load External Plugin")
        self.layout.addWidget(self.load_btn)

        self.setLayout(self.layout)

        self.refresh_list()

        self.toggle_btn.clicked.connect(self.toggle_plugin)
        self.load_btn.clicked.connect(self.load_external)

    def refresh_list(self):
        self.list_widget.clear()

        for p in self.pm.plugins:
            status = "ON" if p["enabled"] else "OFF"
            self.list_widget.addItem(
                f"{p['name']} [{status}] - {p['description']}"
            )

    def toggle_plugin(self):
        index = self.list_widget.currentRow()
        if index < 0:
            return

        plugin = self.pm.plugins[index]
        plugin["enabled"] = not plugin["enabled"]
        plugin["instance"].enabled = plugin["enabled"]

        self.refresh_list()

    def load_external(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Select Plugin File",
            "",
            "Python Files (*.py)"
        )

        if file_path[0]:
            self.pm.load_plugins_from_folder(
                os.path.dirname(file_path[0])
            )
            self.refresh_list()