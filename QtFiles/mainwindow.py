import sys

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from pathlib import Path

import src.RidersPyTools_KC.include.Constants
import src.RidersPyTools_KC.RidersObject
from settingsFunc import load_path
#from Examples.QtFiles import exGearGarage, recordKeeper, timeTrialBuddy
from src.RidersPyTools_KC.MapParser import read_for_list
from exGearGarage import eggWindow
from recordKeeper import recordsWindow
#from src.RidersPyTools_KC.include import Constants
from timeTrialBuddy import ttbWindow
from settingsWindow import settingsWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Jordskatool")
        self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))
        self.background_image_path = "jordskatoolBackground.png"
        self.load_background_image()

        #Buttons
        self.eggButton.clicked.connect(self.openEgg)
        self.ttbButton.clicked.connect(self.openTTB)
        self.recordsButton.clicked.connect(self.openRecords)
        self.settingsButton.clicked.connect(self.openSettings)
        #self.object_overrides = {}


    #these are really ugly dont look at them
    def load_background_image(self):
        image_path = Path(__file__).resolve().parent / self.background_image_path

        pixmap = QtGui.QPixmap(str(image_path))

        if pixmap.isNull():
            print("Failed to load image:", image_path)
            return

        self.backgroundGraphicsView.setStyleSheet("""
            QGraphicsView {
                background: transparent;
                border: none;
            }
        """)
        self.backgroundGraphicsView.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.backgroundGraphicsView.setAutoFillBackground(False)
        self.backgroundGraphicsView.viewport().setAutoFillBackground(False)
        self.backgroundGraphicsView.viewport().setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.backgroundScene = QtWidgets.QGraphicsScene(self)

        self.backgroundPixmapItem = self.backgroundScene.addPixmap(pixmap)
        self.backgroundScene.setSceneRect(self.backgroundPixmapItem.boundingRect())

        self.backgroundGraphicsView.setScene(self.backgroundScene)

        QtCore.QTimer.singleShot(0, self.fit_background_image)

    def fit_background_image(self):
        if not hasattr(self, "backgroundPixmapItem"):
            return

        self.backgroundGraphicsView.resetTransform()

        self.backgroundGraphicsView.fitInView(
            self.backgroundPixmapItem,
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_background_image()

    def openEgg(self):
        self.eggWindow = eggWindow()
        self.eggWindow.show()

    def openTTB(self):
        self.ttbWindow = ttbWindow()
        self.ttbWindow.show()

    def openRecords(self):
        self.recordsWindow = recordsWindow()
        self.recordsWindow.show()

    def debugButtonClicked(self):
        self.settingsWindow = settingsWindow()
        self.settingsWindow.show()

    def openSettings(self):
        self.settingsWindow = settingsWindow()
        self.settingsWindow.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()


    window.show()
    sys.exit(app.exec())