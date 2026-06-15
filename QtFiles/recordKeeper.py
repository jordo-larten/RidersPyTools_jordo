from ttbFunc import dataframe_to_table
import pandas as pd
from PyQt6 import QtWidgets, uic, QtGui
class recordsWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("records.ui", self)
        #uic.loadUi("Examples\QtFiles\\records.ui", self) #run from .bat
        self.setWindowTitle("Records")
        self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))
        self.refreshButton.clicked.connect(self.refresh_func)
        self.sortBox.currentIndexChanged.connect(self.refresh_func)
        self.showAllDataBox.stateChanged.connect(self.refresh_func)
        self.filterList = {"Mode":"Any",
                           "Stage":"Any",
                           "Character":"Any",
                           "Archetype":"Any",
                           "Gear":"Any",
                           "Type":"Any"}
        self.modes,self.stages,self.characters,self.archetypes,self.gears,self.types = [],[],[],[],[],[]
        self.modeBox.currentIndexChanged.connect(self.refresh_func)
        self.stageBox.currentIndexChanged.connect(self.refresh_func)
        self.characterBox.currentIndexChanged.connect(self.refresh_func)
        self.archBox.currentIndexChanged.connect(self.refresh_func)
        self.gearBox.currentIndexChanged.connect(self.refresh_func)
        self.typeBox.currentIndexChanged.connect(self.refresh_func)
        try:
            self.refresh_func()
        except FileNotFoundError:
            print("TimeTable.csv not found, try recording some races with Time Trial Buddy!")
            #ideally this opens a popup saying this^ and options to close, open TTB, and cancel (for sickos)
        except:
            print("Error")


    def populate_boxes(self):
        modes = self.df['Mode'].unique()
        for mode in modes:
            if mode not in self.modes:
                self.modes.append(mode)
                self.modeBox.addItem(mode)

        stages = self.df['Stage'].unique()
        for stage in stages:
            if stage not in self.stages:
                self.stages.append(stage)
                self.stageBox.addItem(stage)

        characters = self.df['Character'].unique()
        for character in characters:
            if character not in self.characters:
                self.characters.append(character)
                self.characterBox.addItem(character)


        archetypes = self.df['Archetype'].unique()
        for archetype in archetypes:
            if archetype not in self.archetypes:
                self.archetypes.append(archetype)
                self.archBox.addItem(archetype)

        gears = self.df['Gear'].unique()
        for gear in gears:
            if gear not in self.gears:
                self.gears.append(gear)
                self.gearBox.addItem(gear)

        types = self.df['Type'].unique()
        for type in types:
            if type not in self.types:
                self.types.append(type)
                self.typeBox.addItem(type)

    def populate_table(self):
        self.get_selections()
        df1 = self.df.copy()
        for key,value in self.filterList.items():
            if value != "Any":
                df1 = df1[df1[key] == value]
        match self.sortBox.currentText():
            case "Ascending (Race Time)":
                df1.sort_values(by=["Raw Final Time"], inplace=True)
            case "Descending (Race Time)":
                df1.sort_values(by=["Raw Final Time"],ascending=False, inplace=True)
            case "Ascending (Timestamp)":
                df1.sort_values(by=["Timestamp"], inplace=True)
            case "Descending (Timestamp)":
                df1.sort_values(by=["Timestamp"], ascending=False, inplace=True)
        if not self.showAllDataBox.isChecked():
            df1 = df1[['Stage','Time','Character','Archetype','Gear','Type','Lap 1','Lap 2','Lap 3','Best Lap']]
        dataframe_to_table(self, df1, self.mainTable)

    def get_selections(self):
        self.filterList["Mode"] = self.modeBox.currentText()
        self.filterList["Stage"] = self.stageBox.currentText()
        self.filterList["Character"] = self.characterBox.currentText()
        self.filterList["Archetype"] = self.archBox.currentText()
        self.filterList["Gear"] =  self.gearBox.currentText()
        self.filterList["Type"] = self.typeBox.currentText()

    def refresh_func(self):
        self.df = pd.read_csv("TimeTable.csv")
        self.populate_boxes()
        self.populate_table()