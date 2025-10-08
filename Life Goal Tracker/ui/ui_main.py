from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from ui.ui_models import Goalbox, makeGoal
from db import return_tables
import os

#Class for main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Goal Tracker")

        # === Central Layout ===
        center = QWidget()
        page = QVBoxLayout(center)
        navigation = QHBoxLayout()

        # === Content Layout ===
        self.content_layout = QHBoxLayout()
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.content_layout.setSpacing(20)

        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(content_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # === Navigation Bar ===
        self.searchbar = QLineEdit()
        self.add = QPushButton("Add Goal")
        self.mode = QPushButton("Dark mode")

        navigation.addStretch()
        navigation.addWidget(QLabel("Search:"))
        navigation.addWidget(self.searchbar)
        navigation.addWidget(self.add)
        navigation.addWidget(self.mode)
        navigation.addStretch()

        # === Assemble Main Layout ===
        page.addLayout(navigation)
        page.addWidget(self.scroll_area)
        self.setCentralWidget(center)

        # === Variables ===
        self.opened_goals = []
        self.dark_mode = True

        # === Connections ===
        self.searchbar.textChanged.connect(lambda text: self.refresh(text))
        self.add.clicked.connect(self.open_goal)
        self.mode.clicked.connect(self.toggle_theme)

        # === Initial Setup ===
        self.refresh()
        self.apply_theme("themes/style.qss")

    # ---------------------------------------------------------
    # ==================== Functions ==========================
    def clear_goals(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    # refreshes the goals to only show what search bar filler text
    def refresh(self, filter_text=""):
        self.clear_goals()
        tables = return_tables()

        for table in tables:
            table_name = table[0]
            pretty_name = table_name.replace("_", " ")

            if filter_text.lower() in pretty_name.lower():
                goalbox = Goalbox(pretty_name)
                self.content_layout.addWidget(goalbox)

    def open_goal(self):
        goal_form = makeGoal(self.content_layout)
        goal_form.show()
        self.opened_goals.append(goal_form)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_theme("ui/themes/style.qss")
            self.mode.setText("Dark mode")
        else:
            self.apply_theme("ui/themes/lightstyle.qss")
            self.mode.setText("Light mode")
            
        with open("ui/theme.txt", "w") as f:
            f.write("dark" if self.dark_mode else "light")

    def apply_theme(self, theme_path):

        if os.path.exists(theme_path):
            with open(theme_path, "r") as style_file:
                QApplication.instance().setStyleSheet(style_file.read())
