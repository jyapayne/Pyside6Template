from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PySide6.QtGui import QIcon
from . import name as project_name

import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(project_name)
        layout = QVBoxLayout()
        label = QLabel("HELLOOOO.")
        label.setMargin(10)
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
