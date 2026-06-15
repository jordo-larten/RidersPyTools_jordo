from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
from settingsFunc import *


class settingsWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("settingsWindow.ui", self)
        self.setWindowTitle("Jordskatool")
        self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))
        self.pathButton.clicked.connect(self.select_build_directory)

        saved_path = load_path()

        if saved_path:
            self.pathLineEdit.setText(saved_path)

    def select_build_directory(self):
        current_path = self.pathLineEdit.text().strip()

        if current_path and Path(current_path).exists():
            start_dir = current_path
        else:
            start_dir = str(Path.home())

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select build directory",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )

        if folder:
            self.pathLineEdit.setText(folder)
            save_path(folder)
