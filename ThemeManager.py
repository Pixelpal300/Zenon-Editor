import os

class ThemeManager:
    def __init__(self, main):
        self.main = main
        self.theme_folder = "themes"

        if not os.path.exists(self.theme_folder):
            os.makedirs(self.theme_folder)

    def save_theme(self, name, qss):
        path = f"{self.theme_folder}/{name}.qss"
        with open(path, "w", encoding="utf-8") as f:
            f.write(qss)

    def apply_theme(self, file):
        path = f"{self.theme_folder}/{file}"

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.main.setStyleSheet(f.read())

    def get_themes(self):
        return [
            f for f in os.listdir(self.theme_folder)
            if f.endswith(".qss")
        ]