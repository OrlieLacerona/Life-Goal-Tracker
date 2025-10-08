from PyQt6.QtWidgets import QApplication
import sys
from ui.ui_main import MainWindow
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__),"ui", "theme.txt")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load last theme
    dark_mode = True
    if os.path.exists(CONFIG_FILE):
        dark_mode = open(CONFIG_FILE).read().strip() == "dark"


    # Create window
    window = MainWindow()
    window.dark_mode = dark_mode

    # Apply theme
    theme_path = "ui/themes/style.qss" if dark_mode else "ui/themes/lightstyle.qss"
    window.apply_theme(theme_path)
    window.mode.setText("Dark mode" if dark_mode else "Light mode")

    window.showMaximized()
    app.exec()
