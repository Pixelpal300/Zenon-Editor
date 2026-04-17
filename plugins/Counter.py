PLUGIN_INFO = {
    "name": "Counter",
    "description": "Shows words, characters, and line count in real time",
    "version": "1.0"
}

class Plugin:
    def __init__(self, editor):
        self.editor = editor
        self.enabled = True

    def activate(self):
        self.editor.textEdit.textChanged.connect(self.update_stats)

    def update_stats(self):
        if not self.enabled:
            return

        text = self.editor.textEdit.toPlainText()

        words = len(text.split())
        chars = len(text)
        lines = len(text.splitlines())

        self.editor.statusBar().showMessage(
            f"Words: {words} | Characters: {chars} | Lines: {lines}"
        )