import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout,
    QPushButton, QMessageBox, QLineEdit, QListWidget
)
from PyQt5.QtCore import Qt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setGeometry(300, 100, 600, 700)
        self.to_do_UI()
        self.load_tasks()

    def to_do_UI(self):
        central_wid = QWidget()
        main_layout = QVBoxLayout()

        self.heading = QLabel("To-Do List 📝")
        self.heading.setStyleSheet("color: navy; font-size: 40px; font-family: Arial; font-weight: bold;")
        self.heading.setAlignment(Qt.AlignCenter)

        input_layout = QVBoxLayout()
        self.input_task = QLineEdit()
        self.input_task.setPlaceholderText("Enter your task...")
        self.input_task.setStyleSheet("font-size: 30px; font-weight: bold; font-family: Arial;")
        self.input_task.setFixedHeight(50)
        self.input_task.returnPressed.connect(self.add_task_event)
        input_layout.addWidget(self.input_task)

        self.add_task = QPushButton("Add Task")
        self.add_task.setStyleSheet("padding: 10px 20px;font-size: 30px; font-family: Arial; background-color: hsl(18, 98%, 50%); color: white; border: 2px solid transparent; border-radius: 20px;")
        self.add_task.clicked.connect(self.add_task_event)
        input_layout.addWidget(self.add_task)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("font-size: 30px; font-weight: bold; font-family: Arial; color: hsl(95, 98%, 49%);")
        self.task_list.itemDoubleClicked.connect(self.toggle_task_status)

        self.delete_task = QPushButton("Delete Task")
        self.delete_task.setStyleSheet("padding: 10px 20px;font-size: 30px; font-family: Arial; background-color: hsl(18, 98%, 50%); color: white; border: 2px solid transparent; border-radius: 20px;")
        self.delete_task.clicked.connect(self.delete_task_event)
        input_layout.addWidget(self.delete_task)

        self.clear_all = QPushButton("Clear All")
        self.clear_all.setStyleSheet("padding: 10px 20px;font-size: 30px; font-family: Arial; background-color: hsl(18, 98%, 50%); color: white; border: 2px solid transparent; border-radius: 20px;")
        self.clear_all.clicked.connect(self.clear_all_event)
        input_layout.addWidget(self.clear_all)

        main_layout.addWidget(self.heading)
        main_layout.addWidget(self.task_list)
        main_layout.addLayout(input_layout)

        central_wid.setLayout(main_layout)
        self.setCentralWidget(central_wid)

    def add_task_event(self):
        task = self.input_task.text().strip().capitalize()
        if task:
            self.task_list.addItem(task)
            self.input_task.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty")

    def delete_task_event(self):
        selected = self.task_list.currentRow()
        if selected >= 0:
            self.task_list.takeItem(selected)
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning", "No task selected")

    def clear_all_event(self):
        self.task_list.clear()
        self.save_tasks()

    def toggle_task_status(self, item):
        font = item.font()
        font.setStrikeOut(not font.strikeOut())
        item.setFont(font)
        self.save_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    text = line.strip()
                    if text.startswith("[x] "):
                        item = text[4:]
                        list_item = self.task_list.addItem(item)
                        item_obj = self.task_list.item(self.task_list.count() - 1)
                        font = item_obj.font()
                        font.setStrikeOut(True)
                        item_obj.setFont(font)
                    else:
                        self.task_list.addItem(text)

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for i in range(self.task_list.count()):
                item = self.task_list.item(i)
                prefix = "[x] " if item.font().strikeOut() else ""
                file.write(prefix + item.text() + "\n")

def main():
    app = QApplication(sys.argv)
    my_window = Window()
    my_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
