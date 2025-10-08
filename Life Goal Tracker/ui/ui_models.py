from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import re
from db import *


# Class that creates goal containers
class makeGoal(QWidget):
    def __init__(self, target_layout):
        super().__init__()
        self.setWindowTitle("Make Goal")
        self.target_layout = target_layout
        self.layout = QVBoxLayout()

        self.name = QLineEdit()
        self.btn = QPushButton("Add Goal") 

        self.layout.addWidget(QLabel("Name of Goal"))
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.btn)

        self.btn.clicked.connect(self.make)
        self.setLayout(self.layout)

    def make(self):
        goal_input = self.name.text().strip()
        if not goal_input or goal_input[0].isdigit():
            QMessageBox.warning(self, "Invalid Goal Name", "Goal name must not start with a number or be blank")
            return
        
        table_name = re.sub(r'\W+', '_', goal_input)
        if table_exists(table_name):
            QMessageBox.warning(self, "Goal Exists", f"A goal with the name '{self.name.text()}' already exists!")
        else:
            create_table(table_name)
            goalbox = Goalbox(table_name)
            self.target_layout.addWidget(goalbox)
            self.close()

#Defines Goalboxes
class Goalbox(QWidget):
    def __init__(self, Goalname="Goal"):
        super().__init__()
        self.name = Goalname
        self.windows = []

        layout = QVBoxLayout()
        navigation = QHBoxLayout()

        content_widget = QWidget()
        content_widget.setObjectName("contentBox")
        content = QVBoxLayout(content_widget)

        self.goalcontainer = QVBoxLayout()
        self.goalcontainer.setContentsMargins(0, 0, 0, 0)

        self.goalcontainer_widget = QWidget()
        self.goalcontainer_widget.setLayout(self.goalcontainer)
        self.goalcontainer_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        wrapper_layout = QVBoxLayout()
        wrapper_layout.addWidget(self.goalcontainer_widget)
        wrapper_layout.addStretch(0)
        wrapper_widget = QWidget()
        wrapper_widget.setObjectName("wrapper")
        wrapper_widget.setLayout(wrapper_layout)
        self.scroll_area.setWidget(wrapper_widget)
        self.scroll_area.setFixedHeight(760)

        title = QLabel(self.name)
        title.setObjectName("title")

        delete_goal = QPushButton("Delete goal")
        mark_done = QPushButton("Submit Finished Tasks")
        navigation.addWidget(title)
        navigation.addWidget(delete_goal)
        navigation.addWidget(mark_done)

        add_btn = QPushButton("Add Task")
        add_btn.setFixedHeight(50)
        content.addWidget(add_btn)
        content.addWidget(self.scroll_area)

        add_btn.clicked.connect(self.addTask)
        mark_done.clicked.connect(self.remove_finished_tasks)
        delete_goal.clicked.connect(self.remove_goal)

        self.load_content()
        layout.addLayout(navigation)
        content.addStretch(1)
        layout.addWidget(content_widget)
        self.setLayout(layout)
        self.setFixedWidth(550)

    def remove_finished_tasks(self):
        delete_completed_tasks(self.name)
        self.load_content()

    def remove_goal(self):
        delete_table(self.name)
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
        self.setParent(None)
        self.deleteLater()

    def addTask(self):
        new_window = addGoal(self.name, parent_goalbox=self)
        new_window.show()
        self.windows.append(new_window)

    def load_content(self):
        """"
        [while loop] - clears all goal containers before putting in the new set
        [For goals in goals] - checks the type of goal and makes the appropriate container
        """
        while self.goalcontainer.count():
            item = self.goalcontainer.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        goals = read_goals(self.name)
        for goal in goals:
            if goal[1] == "progressTask":
                widget = progressTask(goal[0],goal[2], goal[3], goal[5], goal[4], self.name)
            elif goal[1] == "checkboxTask":
                widget = checkboxTask(goal[2], goal[3], self.name, goal[6])
            else:
                continue
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.goalcontainer.addWidget(widget)

        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(0))

# Window that appears when you add a task 
# addgoal splits into two parts -initial- -specific- as each type of tasks wants specific inputs
# Note: Only progressTask is in use currently
class addGoal(QWidget):
    def __init__(self,goalname,parent_goalbox=None):
        super().__init__()
        self.setWindowTitle("Add task")
        self.task_widget = None
        self.name = goalname
        self.parent_goalbox = parent_goalbox
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel(f"Type of Task"))

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Progress Task"])
        self.dropdown.currentIndexChanged.connect(self.change)
        self.layout.addWidget(self.dropdown)

        self.layout.addWidget(QLabel(f"Title of Task"))
        self.title = QLineEdit()

        self.layout.addWidget(self.title)



        self.change()
        self.setLayout(self.layout)

    def change(self):
        if self.task_widget:
            self.layout.removeWidget(self.task_widget) 
            self.task_widget.setParent(None)            
            self.task_widget.deleteLater()             
            self.task_widget = None                      
            
        if self.dropdown.currentText() == "Progress Task":
            
            self.task_widget = addGoalProgressTask(self.title,self.name)
            self.layout.addWidget(self.task_widget)
        
        """
        Phased out this segment as it is not being utilized as of the moment

        elif self.dropdown.currentText() == "Checkbox Task":
            self.task_widget = addGoalCheckboxTask(self.title)
            self.layout.addWidget(self.task_widget)
            pass
        elif self.dropdown.currentText() == "Checker Task":
            self.task_widget = addGoalCheckTask()
            self.layout.addWidget(self.task_widget)
            
        """
 

# -specific- for ProgressTask
class addGoalProgressTask(QWidget):
    def __init__(self,title_input,goalname):
        super().__init__()
        self.title_input = title_input 
        self.number = 1
        self.name = goalname

        self.layout = QVBoxLayout()

        containerA = QVBoxLayout()
        containerB = QHBoxLayout()


        self.description = QTextEdit()

        add_btn = QPushButton("+")
        subtract_btn = QPushButton("-")

        self.progress = QLabel(f"Progress Amount: {self.number}")
        containerB.addWidget(self.progress)
        containerB.addWidget(add_btn)
        containerB.addWidget(subtract_btn)

        containerA.addWidget(QLabel(f"Description: "))
        containerA.addWidget(self.description)

        containerA.addLayout(containerB)

        add_btn.clicked.connect(self.progressup)
        subtract_btn.clicked.connect(self.progressdown)

        
        containerB.addWidget(add_btn)
        containerB.addWidget(subtract_btn)
        self.layout.addLayout(containerA)
        self.add = QPushButton("Add Task")
        self.layout.addWidget(self.add)
        self.setLayout(self.layout)

        self.add.clicked.connect(self.click)
    
    #==================== Functions ===================
    def click(self):
        add_goal("progressTask", self.title_input.text(), self.description.toPlainText(), 0, self.number, self.name,0)
        if hasattr(self.parent(), 'parent_goalbox') and self.parent().parent_goalbox:
            self.parent().parent_goalbox.load_content()
        self.parent().close()

    def progressup(self):
        self.number += 1
        self.update_progress_label()
        pass
    def progressdown(self):
        if self.number > 1:
            self.number -= 1
            self.update_progress_label()
            pass
    def update_progress_label(self):
        self.progress.setText(f"Progress Amount: {self.number}")

#types = progess, checkbox, check
#ProgressTask Container
class progressTask(QWidget):
    def __init__(self,id, taskname,description,max=1,current=0,table=""):
        super().__init__()
        self.setObjectName("progressTask")
        self.id = id
        self.table = table
        self.name = taskname
        self.description = description
        self.max = max
        self.current = current
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        left = QVBoxLayout()
        content = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(content)
        content_widget.setObjectName("progressContent")
        right = QVBoxLayout()

        add_btn = QPushButton("+")
        left.addWidget(add_btn)
        subtract_btn = QPushButton("-")
        right.addWidget(subtract_btn)

        add_btn.setObjectName("plusButton")
        subtract_btn.setObjectName("minusButton")

        add_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        subtract_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        title_label = QLabel(self.name)
        title_label.setObjectName("progressTitle")
        content.addWidget(title_label)

        desc_label = QLabel(self.description)
        desc_label.setWordWrap(True)
        content.addWidget(desc_label)

        self.progressview = QLabel(f"{self.current} | {self.max}")
        view = QHBoxLayout()
        view.addStretch(1)
        view.addWidget(self.progressview)
        content.addLayout(view)

        layout.addLayout(left)
        layout.addWidget(content_widget) 
        layout.addLayout(right)

    

        add_btn.clicked.connect(self.progressup)
        subtract_btn.clicked.connect(self.progressdown)
        self.setLayout(layout)
        self.setMinimumSize(300, 100)

    #===================== FUNCTIONS ===================

    def progressup(self):
        if self.current < self.max:
            self.current += 1
            self.update_progress()
            pass
    def progressdown(self):
        if self.current > 0:
            self.current -= 1
            self.update_progress()
            pass
    def update_progress(self):
        self.progressview.setText(f"{self.current} | {self.max}")
        modify_current(self.table, self.id, self.current)





#================================= SEGMENT BELOW CURRENTLY NOT IN USE ===================================================
#================================= SEGMENT BELOW IS FOR UPSCALING APP ===================================================
#================================= SEGMENT BELOW CURRENTLY NOT IN USE ===================================================
#================================= SEGMENT BELOW CURRENTLY NOT IN USE ===================================================

# -specific- for Checkbox task
# CURRENTLY NOT IN USE
class addGoalCheckboxTask(QWidget):
    def __init__(self,title_input):
        super().__init__()

        self.title_input = title_input 
        self.layout = QVBoxLayout()
        
    
        self.description = QTextEdit()

        self.layout.addWidget(QLabel("Description"))
        self.layout.addWidget(self.description)

        self.add = QPushButton("Add Task")
        self.layout.addWidget(self.add)
        self.add.clicked.connect(self.click)

        self.setLayout(self.layout)

    def click(self):
        add_goal("checkboxTask", self.title_input.text(), self.description.toPlainText(), 0, 0, self.parent().name,0)
        if hasattr(self.parent(), 'parent_goalbox') and self.parent().parent_goalbox:
            self.parent().parent_goalbox.load_content()
        self.parent().close()

class addGoalCheckTask(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.Subtask = QLineEdit()
        self.addsubtask = QPushButton("Add Subtask")
        self.layout.addWidget(QLabel("Subtask title"))
        self.layout.addWidget(self.Subtask)
        self.layout.addWidget(self.addsubtask)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  
        self.container_widget = QWidget()          
        self.container_layout = QVBoxLayout(self.container_widget)
        self.scroll_area.setWidget(self.container_widget)
        self.layout.addWidget(self.scroll_area)


        add = QPushButton("Add Task")
        self.layout.addWidget(add)

        self.setLayout(self.layout)


        self.addsubtask.clicked.connect(self.addsub)

    def addsub(self):
        if self.Subtask.text():  
            self.container_layout.addWidget(subtask(self.Subtask.text()))



class subtask(QWidget):
    def __init__(self, name):
        super().__init__()
        self.layout = QHBoxLayout()
        checkbox = QCheckBox(name)
        self.layout.addWidget(checkbox)
        self.setLayout(self.layout)





class checkboxTask(QWidget):
    def __init__(self, taskname,description,table="",done=0):
        super().__init__()
        self.table = table
        self.name = taskname
        self.description = description
        self.done = done
        

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        left = QVBoxLayout()
        content = QVBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        self.checkbox = QCheckBox()

        content.addLayout(left)
        content.addWidget(QLabel(self.name))
        content.addWidget(QLabel(self.description))

        

        layout.addWidget(self.checkbox)
        layout.addLayout(content)


        self.setLayout(layout)
        self.setMinimumSize(300, 100)
        self.setMaximumSize(300, 100)

        self.initial()
        self.checkbox.clicked.connect(self.check)

    def initial(self):
        self.checkbox.setChecked(bool(self.done))


    def check(self): 
        self.done = 1 if self.checkbox.isChecked() else 0

        if self.table:
            modify_done(self.table, self.name, self.done)


        
         
class checkTask(QWidget):
    def __init__(self, taskname,tasks):
        super().__init__()
        self.name = taskname
        self.tasks = tasks
        layout = QHBoxLayout()
        content = QVBoxLayout()
        task_container = QVBoxLayout()

        
        

        for item in tasks:
            task_container.addWidget(QCheckBox(item))
            pass

        content.addWidget(QLabel(self.name))
        content.addLayout(task_container)
        layout.addLayout(content)


        self.setLayout(layout)
        self.setMinimumSize(300, 100)