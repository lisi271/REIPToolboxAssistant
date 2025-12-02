from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from .styles import TASK_CARD_STYLE


class TaskWidget(QFrame):
    def __init__(self, task):
        super().__init__()
        self.task = task

        self.setStyleSheet(TASK_CARD_STYLE)

        layout = QVBoxLayout()

        title = QLabel(f"<b>{task.title}</b>")
        layout.addWidget(title)

        tags_row = QHBoxLayout()
        for tag in task.tags:
            tag_label = QLabel(f"[{tag}]")
            tags_row.addWidget(tag_label)
        layout.addLayout(tags_row)

        date = QLabel(f"📅 {task.date}")
        layout.addWidget(date)

        note = QLabel(f"📝 {task.note if task.note else 'No note'}")
        layout.addWidget(note)

        open_btn = QPushButton("Open in Toolbox")
        open_btn.clicked.connect(self.open_url)
        layout.addWidget(open_btn)

        self.setLayout(layout)

    def open_url(self):
        if self.task.url:
            QDesktopServices.openUrl(QUrl(self.task.url))
