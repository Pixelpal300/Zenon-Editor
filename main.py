from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QActionGroup
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QIcon

import sys

from colordialog import ColorDialog
from FontDialog import FontDialog
from FontSizeDialog import FontSizeDialog
from SaveDialog import SaveDialog
from plugin_manager import PluginManager
from PluginDialog import PluginDialog
from ThemeManager import ThemeManager
from ThemeBrowser import ThemeBrowser
from fileinfo import show_file_info
from utils import resource_path



class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi(resource_path("UI", "Text_editor_ui.ui"), self)

        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_plugins_from_folder(resource_path("plugins"))
        self.theme_manager = ThemeManager(self)

        self.current_fpath = None
        self.is_modified = False

        self.alignGroup = QActionGroup(self)
        
        self.setWindowTitle('Untitled')
        self.textEdit.setAlignment(Qt.AlignLeft)
        
        self.alignGroup.setExclusive(True)
        self.actionAlignLeft.setChecked(True)
        self.actionBold.setCheckable(True)

        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)

        self.actionAlignLeft.setCheckable(True)
        self.actionAlign_Center.setCheckable(True)
        self.actionAlign_Right.setCheckable(True)
        self.actionAlign_Justify.setCheckable(True)

        self.actionItallic.setCheckable(True)
        self.actionUnderline.setCheckable(True)

        self.alignGroup.addAction(self.actionAlignLeft)
        self.alignGroup.addAction(self.actionAlign_Center)
        self.alignGroup.addAction(self.actionAlign_Right)
        self.alignGroup.addAction(self.actionAlign_Justify)


        self.actionNew_File.triggered.connect(self.New_file)
        self.actionSave.triggered.connect(self.Save_file)
        self.actionSave_As.triggered.connect(self.Save_file_as)
        self.actionOpen.triggered.connect(self.Open_file)
        self.actionHelp.triggered.connect(self.help)

        self.textEdit.textChanged.connect(self.mark_modified)
        self.actionPlugins.triggered.connect(self.open_plugins)
        self.actionFile_info.triggered.connect(self.open_file_info)
        self.actionSelect_Font.triggered.connect(self.change_Font)
        self.actionFont_Size.triggered.connect(self.change_Font_Size)
        self.actionThemes.triggered.connect(self.open_theme_manager)
        
        self.actionFont_Color.triggered.connect(self.change_Font_color)
        self.actionUnderline.triggered.connect(lambda : self.textEdit.setFontUnderline(self.actionUnderline.isChecked()))
        self.actionItallic.triggered.connect(lambda : self.textEdit.setFontItalic(self.actionItallic.isChecked()))
        self.actionBold.triggered.connect(self.toggle_bold)
        
        self.actionUndo.triggered.connect(lambda : self.textEdit.undo())
        self.actionRedo.triggered.connect(lambda : self.textEdit.redo())
        self.actionCut.triggered.connect(lambda : self.textEdit.cut())
        self.actionCopy.triggered.connect(lambda : self.textEdit.copy())
        self.actionPaste.triggered.connect(lambda : self.textEdit.paste())
       
        self.actionAlignLeft.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignLeft))
        self.actionAlign_Center.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignCenter))
        self.actionAlign_Right.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignRight))
        self.actionAlign_Justify.triggered.connect(lambda: self.textEdit.setAlignment(Qt.AlignJustify))

    def maybe_save(self):
        if not self.is_modified:
            return True

        dialog = SaveDialog(self)
        result = dialog.exec()

        if dialog.choice == "save":
            self.Save_file()
            return not self.is_modified

        elif dialog.choice == "discard":
            return True

        return False

    def open_file_info(self):
        text = self.textEdit.toPlainText()
        file_path = self.current_fpath

        show_file_info(self, text, file_path)
    
    def open_theme_manager(self):
        self.theme_window = ThemeBrowser(self.theme_manager)
        self.theme_window.exec()

    def open_plugins(self):
        dialog = PluginDialog(self.plugin_manager)
        dialog.exec()

    def mark_modified(self):
        self.is_modified = True
        if not self.windowTitle().endswith("*"):
            self.setWindowTitle(self.windowTitle() + "*")

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

            
    def toggle_bold(self):
        cursor = self.textEdit.textCursor()
        fmt = QTextCharFormat()

        if cursor.charFormat().fontWeight() == QFont.Bold:
            fmt.setFontWeight(QFont.Normal)
        else:
            fmt.setFontWeight(QFont.Bold)

        cursor.mergeCharFormat(fmt)
        self.textEdit.setTextCursor(cursor)
    
    def get_text(self):
        return self.text_edit.toPlainText()

    def change_Font_Size(self):
        self.font_dialog = FontSizeDialog(self)
        self.font_dialog.show()


    def New_file(self):
        if not self.maybe_save():
            return

        self.textEdit.clear()
        self.current_fpath = None
        self.setWindowTitle("Untitled")
        self.is_modified = False

    def Open_file(self):
        path = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "HTML Files (*.html *.myhtml)"
        )

        if not path[0]:
            return

        with open(path[0], "r", encoding="utf-8") as f:
            html = f.read()

        self.textEdit.setHtml(html)
        self.current_fpath = path[0]
        self.setWindowTitle(path[0])
        self.is_modified = False

    def update_color(self):
        r = self.RedSlider.value()
        g = self.GreenSlider.value()
        b = self.BlueSlider.value()

        self.previewBox.setStyleSheet(f"""
            background-color: rgb({r}, {g}, {b});
            border: 2px solid white;
            border-radius: 10px;
        """)

        self.RedValue.setText(str(r))
        self.GreenValue.setText(str(g))
        self.BlueValue.setText(str(b))

        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.HexCodeLine.setText(hex_color)
    
    def hex_changed(self):
        text = self.HexCodeLine.text().strip()

        if not text.startswith("#"):
            text = "#" + text

        color = QColor(text)

        if color.isValid():
            r = color.red()
            g = color.green()
            b = color.blue()

            self.RedSlider.setValue(r)
            self.GreenSlider.setValue(g)
            self.BlueSlider.setValue(b)

    def Save_file_as(self):
        path = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "My Editor (*.myhtml);;HTML (*.html)"
        )

        if not path[0]:
            return

        file_path = path[0]

        if not file_path.endswith(".html"):
            file_path += ".html"

        html = self.textEdit.toHtml()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.current_fpath = file_path
        self.setWindowTitle(file_path)
        self.is_modified = False


    def Bold(self):
        if self.actionBold.isChecked():
            self.textEdit.setFontWeight(QFont.Bold)
        else:
            self.textEdit.setFontWeight(QFont.Normal)

    def help(self):
        pass
    
    def change_Font(self):
        self.font_dialog = FontDialog(self)
        self.font_dialog.show()
        
    def change_Font_color(self):
        self.color_dialog = ColorDialog(self)
        self.color_dialog.show()
    

    def Save_file(self):
        if self.current_fpath:
            with open(self.current_fpath, "w", encoding="utf-8") as file:
                file.write(self.textEdit.toHtml())

            self.is_modified = False
            self.setWindowTitle(self.current_fpath)

        else:
            self.Save_file_as()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("Logo.png")))
    ui = Main()
    ui.show()
    app.exec_()