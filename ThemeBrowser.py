from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
from utils import resource_path

class ThemeEditor(QDialog):
    def __init__(self, theme_manager, theme_file):
        super().__init__()

        self.tm = theme_manager
        self.file = theme_file
        self.setWindowIcon(resource_path(QIcon("Logo.png")))
        self.setWindowTitle(f"Editing Theme: {theme_file}")
        self.resize(600, 400)

        self.setStyleSheet("""
        QDialog {
            background-color: #181b28;
            color: white;
        }

        QTextEdit {
            background-color: #181b28;
            color: white;
            border: 1px solid #2a2f45;
        }

        QPushButton {
            background-color: #181b28;
            color: white;
            border: 1px solid #2a2f45;
        }

        QPushButton:hover {
            background-color: #2a2f45;
        }
        """)

        layout = QVBoxLayout()

        self.editor = QTextEdit()
        layout.addWidget(self.editor)

        self.save_btn = QPushButton("Save Changes")
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_file()

        self.save_btn.clicked.connect(self.save_file)

    def load_file(self):
        path = f"{self.tm.theme_folder}/{self.file}"

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_file(self):
        path = f"{self.tm.theme_folder}/{self.file}"

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())

            msg = QMessageBox(self)
            msg.setWindowTitle("Saved")
            msg.setText("Theme updated successfully!")

            msg.setStyleSheet("""
            QMessageBox {
                background-color: #181b28;
                color: white;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #181b28;
                color: white;
                border: 1px solid #2a2f45;
            }
            """)

            msg.exec_()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ThemeBrowser(QDialog):
    def __init__(self, theme_manager):
        super().__init__()

        self.tm = theme_manager

        self.setWindowTitle("Theme Manager")
        self.resize(400, 350)

        self.setStyleSheet("""
        QWidget {
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
        }

        QPushButton:hover {
            background-color: #2a2f45;
        }
        """)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.apply_btn = QPushButton("Apply Theme")
        self.save_btn = QPushButton("Create New Theme")
        self.edit_btn = QPushButton("Edit Theme")
        self.refresh_btn = QPushButton("Refresh")
        self.reset_btn = QPushButton("Reset to Default Theme")

        layout.addWidget(self.reset_btn)
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)

        self.load_themes()

        self.apply_btn.clicked.connect(self.apply_theme)
        self.save_btn.clicked.connect(self.save_theme)
        self.edit_btn.clicked.connect(self.edit_theme)
        self.refresh_btn.clicked.connect(self.load_themes)
        self.reset_btn.clicked.connect(self.reset_theme)

    def load_themes(self):
        self.list_widget.clear()

        themes = self.tm.get_themes()

        if not themes:
            self.list_widget.addItem("No themes found")
            return

        for t in themes:
            self.list_widget.addItem(t)

    def reset_theme(self):
        self.tm.main.setStyleSheet("")

        msg = QMessageBox(self)
        msg.setWindowTitle("Theme Reset")
        msg.setText("Default theme restored successfully!")

        msg.setStyleSheet("""
        QMessageBox {
            background-color: #181b28;
            color: white;
        }

        QLabel {
            color: white;
        }

        QPushButton {
            background-color: #181b28;
            color: white;
            border: 1px solid #2a2f45;
        }
        """)

        msg.exec_()

    def apply_theme(self):
        item = self.list_widget.currentItem()

        if not item:
            return

        if item.text() == "No themes found":
            return

        self.tm.apply_theme(item.text())

    def save_theme(self):
        name, ok = QInputDialog.getText(self, "Save Theme", "Theme name:")

        if ok and name:
            qss = self.tm.main.styleSheet()
            self.tm.save_theme(name, qss)

            msg = QMessageBox(self)
            msg.setWindowTitle("Saved")
            msg.setText(f"Theme '{name}' saved!")

            msg.setStyleSheet("""
            QMessageBox {
                background-color: #181b28;
                color: white;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background-color: #181b28;
                color: white;
                border: 1px solid #2a2f45;
            }
            """)

            msg.exec_()

            self.load_themes()

    def edit_theme(self):
        item = self.list_widget.currentItem()

        if not item:
            return

        if item.text() == "No themes found":
            return

        self.editor_window = ThemeEditor(self.tm, item.text())
        self.editor_window.exec()