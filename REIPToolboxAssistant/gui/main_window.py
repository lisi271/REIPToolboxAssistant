from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from backend.api_client import ToolboxAPI
from .task_widget import TaskWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api = ToolboxAPI()

        self.setWindowTitle("RE-IP Toolbox Assistant")
        self.setGeometry(200, 100, 850, 600)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.refresh_btn = QPushButton("🔄 Refresh Tasks")
        self.refresh_btn.clicked.connect(self.load_tasks)
        self.layout.addWidget(self.refresh_btn)

        self.status_label = QLabel("Status: Connected")
        self.layout.addWidget(self.status_label)

        self.tasks_area = QScrollArea()
        self.tasks_area.setWidgetResizable(True)
        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_area.setWidget(self.tasks_widget)

        self.layout.addWidget(self.tasks_area)

        self.setCentralWidget(self.container)

    def load_tasks(self):
        tasks = self.api.get_tasks()
        self.clear_tasks()

        for task in tasks:
            widget = TaskWidget(task)
            self.tasks_layout.addWidget(widget)

    def clear_tasks(self):
        for i in reversed(range(self.tasks_layout.count())):
            item = self.tasks_layout.itemAt(i).widget()
            item.deleteLater()
