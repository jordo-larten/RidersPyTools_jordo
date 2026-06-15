from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.GameState import MODE_ID_TO_NAME, ExitMethod, RaceState
from src.RidersPyTools_KC.RidersObject import RidersObject

from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
import pandas as pd
#import datetime
import time
#credit for this function is to Kid.Chameleon / KungfuKaphwan / KidWizardOfTheWeb / BattleBornRuffian / ReaperCo CEO
def convert_centi(centi):
    # Divide centiseconds to get minutes and seconds
    centi = centi / 100

    # Divide into minutes and seconds
    minutes, seconds = divmod(centi, 60)

    # Divide into seconds and centiseconds
    seconds, centiseconds = divmod(seconds, 1)

    # Round centiseconds to 2 places just like in-game
    centiseconds = round(centiseconds, 2) * 100

    return [minutes, seconds, centiseconds]
#overrides for 2.4.6.1
object_overrides = {
        "CurrentGameMode": 0x8053C2E0,
        "geGame_ModeDetail": 0x8053C2E4,
        "CurrentStage": 0x8053C2E8,
        "ExitMethod": 0x8053C300,
        "StageTimer": 0x8053C480
}
#format to match in-game timer style
timerTemplate = "{:02d}'{:02d}\"{:02d}"
#type lookup shortcut
type_lookup = {
        1: "Speed",
        2: "Fly",
        3: "Speed/Fly",
        4: "Power",
        5: "Speed/Power",
        6: "Power/Fly",
        7: "Omnitype",
        8: "No type"
}

class ridersTime:
    def __init__(self,centi):
        self.totalCenti = centi
        self.min, self.sec, self.centi = convert_centi(centi)
        self.prettyTime = timerTemplate.format(int(self.min), int(self.sec), int(self.centi))

class timeTrialEntry:
    def __init__(self,player,ridersObject):
        try:
            character = CHR_ID_TO_NAME[player.character]
        except KeyError:
            character = str(player.character)
        try:
            archetype = ARCH_ID_TO_NAME[player.characterArchetype]
        except KeyError:
            archetype = str(player.characterArchetype)
        try:
            gear = GEAR_ID_TO_NAME[player.extremeGear]
        except KeyError:
            gear = str(player.extremeGear)
        try:
            stage = STAGE_ID_TO_NAME[ridersObject.currentStage]
        except KeyError:
            stage = str(ridersObject.currentStage)
        try:
            mode = MODE_ID_TO_NAME[ridersObject.currentMode]
        except KeyError:
            mode = str(ridersObject.currentMode)
        try:
            type = type_lookup[player.typeAttributes]
        except KeyError as e:
            print(e)
            type = str(player.typeAttributes)

        lap1Time = ridersTime(int(player.lapTimeList[0]))
        lap2Time = ridersTime(int(player.lapTimeList[1]))
        lap3Time = ridersTime(int(player.lapTimeList[2]))
        finalTime = ridersTime(int(player.lastSplitLapTime))
        rawLaps = [lap1Time.totalCenti, lap2Time.totalCenti, lap3Time.totalCenti]
        bestLap = rawLaps.index(min(rawLaps))
        bestLapTime = ridersTime(rawLaps[bestLap])

        self.df = pd.DataFrame(
            [{
            "Mode": mode,
            "Stage": stage,
            "Time": finalTime.prettyTime,
            "Character": character,
            "Archetype": archetype,
            "Gear": gear,
            "Type": type,
            "Lap 1": lap1Time.prettyTime,
            "Lap 2": lap2Time.prettyTime,
            "Lap 3": lap3Time.prettyTime,
            "Best Lap": bestLap + 1,
            "Best Lap Time": bestLapTime.prettyTime,
            "Raw Lap 1 Time": lap1Time.totalCenti,
            "Raw Lap 2 Time": lap2Time.totalCenti,
            "Raw Lap 3 Time": lap3Time.totalCenti,
            "Raw Best Lap Time": rawLaps[bestLap],
            "Raw Final Time": finalTime.totalCenti,
            #"Timestamp": datetime.datetime.now()
            "Timestamp": time.time()
              }],
        )
def dataframe_to_table(self, df, table):
    table.clear()

    table.setRowCount(len(df))
    table.setColumnCount(len(df.columns))
    table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())

    for row in range(len(df)):
        for col in range(len(df.columns)):
            value = df.iloc[row, col]
            text = "" if pd.isna(value) else str(value)

            table.setItem(row, col, QTableWidgetItem(text))

    table.resizeColumnsToContents()
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)