
<h1 align="center"> Life Goal Tracker </h1>

<p align="center">
  <i>A clean and minimal goal tracking app built with Python (PyQt6).</i><br>
  <b>Track, organize, and visualize your personal goals - all in one place. -</b>
</p>

---

## Proponent(s)
**Orlie Louise E. Lacerona** – BSCS  

---

## Project Overview
This project is a Life Goal Management System designed to help it's users track and visualize their goals. 
It allows users to create categories for their goals and descriptions for each tasks, specifically designed with a user-friendly interface. 
This program was developed using Python (PyQt6) and uses QSS (QT Style Sheet) for it's UI styling.

---

## Features
- **Create, View, and Manage Goals**
- **Organized Layouts using multiple windows and containers as templates** 
- **Theme switch ( light/dark mode )**
- **Dynamic updates lists to what user inputs**
- **Styled and Minimalistic**

---

## Code Design and Structure  

- `main.py` - Launches the application, applies the stylesheet, and opens the main window
- `db.py` - Contains database logic and commands used to store tasks and goals
- `ui/` - Folder that contains all the UI components and layout logic
  - `themes/` - Folder that contains the stylesheet for different themes
  - `theme.txt` - Text file that contains your current theme preference
  - `ui_main.py` - Class for the main window and handles interactions
  - `ui_models.py` - Contains the templates for containers and interaction logic for each container

---

## Screenshots








**[Main window]**<img width="1721" height="810" alt="Screenshot 2025-10-09 004909" src="https://github.com/user-attachments/assets/d09978a3-34b9-430f-89e0-f7ff7932f612" />
**[Light mode]**<img width="1775" height="600" alt="Screenshot 2025-10-09 054855" src="https://github.com/user-attachments/assets/c2b5ae94-de9a-4b14-9fc4-fbdc883813fb" />
**[Search]**<img width="1544" height="443" alt="Screenshot 2025-10-09 005114" src="https://github.com/user-attachments/assets/5e294767-5744-4fe5-9d8e-65e1069603b7" />
<img width="315" height="502" alt="Screenshot 2025-10-09 005044" src="https://github.com/user-attachments/assets/a83e5f1f-ff8e-489b-9d5d-f98c2efde2ca" />
<img width="235" height="187" alt="Screenshot 2025-10-09 005053" src="https://github.com/user-attachments/assets/bc0f2194-6fe4-4e1b-aabf-4b857abcab9e" />


---

## How to Run the Program

Follow these steps to run the Goal Tracker application:

1. **Install Python 3.x**  
   Make sure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install required packages**  
   Open a terminal or command prompt in your project folder and run:
   ```bash
   pip install PyQt6
   
3. **Navigate to the project directory**
   Use the terminal to go to the folder containing main.py.
   ```bash example
   cd "c:\Users\Name\File_path"

5. **Run the application**
  Execute the main file using:
   ```bash
    python main.py
  
6. **Use the application**
    The main window will open maximized.
    Use the Add Goal button to create new goals.
    Use the Dark/Light Mode button to switch themes.
    Add tasks to each goal and track progress.

<h1>Make sure the ui/themes/style.qss and ui/themes/lightstyle.qss files exist in the correct folders, 
or the theme may not load correctly.</h1>

