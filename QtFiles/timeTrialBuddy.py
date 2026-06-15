from QtFiles.settingsFunc import load_path
from ttbFunc import *
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from eggFunc import check_DME_hook, get_player
import time
import pandas as pd

if not load_path():

    object_overrides = {
            "CurrentGameMode": 0x8053C2E0,
            "geGame_ModeDetail": 0x8053C2E4,
            "CurrentStage": 0x8053C2E8,
            "RaceExitMethod": 0x8053C300,
            "StageTimer": 0x8053C480
        }
else:
    object_overrides = {}


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
timerTemplate = "{:02d}'{:02d}\"{:02d}"

class ttbWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("timeTrialBuddy.ui", self)
        self.setWindowTitle("Time Trial Buddy")
        self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))

        self.dmeHookButton.clicked.connect(check_DME_hook)
        self.loadStateButton.clicked.connect(self.load_state)
        self.lastCheckedLap = 0
        self.buddyDaemon = QtCore.QTimer()
        self.buddyDaemon.setInterval(200)
        self.buddyDaemon.timeout.connect(self.buddy_daemon)
        self.daemon_heartbeat = QtCore.QTimer()
        self.daemon_heartbeat.setInterval(500)
        self.daemon_heartbeat.start()
        self.daemon_heartbeat.timeout.connect(self.daemon_heartbeat_func)
        self.jordoButton.clicked.connect(self.jordo_func)
        self.refreshRecordsButton.clicked.connect(self.refresh_records)
        self.altBox.currentIndexChanged.connect(self.refresh_records)
        self.resetButton.clicked.connect(self.reset_session)
        self.bestLap = -1
        self.bestLapTimeSession = -1
        self.bestTimeCurrentBuild = -1
        self.bestTimeStage = -1
        self.retries = 0
        self.bestSessionTime = 0
        self.sessionRuns = 0

        #self.buddyDaemon.start()

    def load_csv(self):
        self.recordsDf = pd.read_csv("TimeTable.csv")
        #get the best time for the stage

        self.bestTimeStage
        self.bestTimeCurrentBuild

    def jordo_func(self):
        print(self.ridersObject.get_race_state())
        print("x")
        print(RaceState.Countdown)
        print("b")
        print(self.ridersObject.get_race_state() == RaceState.Countdown)

    def race_end_func(self):
        if self.recordTimeChkBox.isChecked():
            entry = timeTrialEntry(self.player, self.ridersObject).df
            try:
                print("Saving race...")
                timeTable = pd.read_csv("TimeTable.csv")
                df = pd.concat([timeTable, entry],ignore_index=True)
                df.to_csv("TimeTable.csv",index=False)
                print("Race saved.")
            except:
                print("TimeTable.csv not found, creating...")
                #df = pd.concat([timeTable, entry], ignore_index=True)
                entry.to_csv("TimeTable.csv",index=False)
                print("TimeTable.csv created.")
            #except:
                #print("oops")
        finishTime = int(self.player.lastSplitLapTime)
        finishTimePretty = ridersTime(finishTime).prettyTime
        # if you beat the best session time (also instantiate it)
        if self.sessionRuns == 0 or self.bestSessionTime > finishTime:
            print("New Session Record: " + finishTimePretty)
            self.bestSessionTime = finishTime
            self.bestSessionTimeLabel.setText(finishTimePretty)
        # if you beat your best time on stage
        if self.bestTimeStage > finishTime:
            print("New Stage Record: " + finishTimePretty)
            self.bestTimeStage = finishTime
            self.bestTimeStageLabel.setText(finishTimePretty)
        # if you beat your best time on pick
        if self.bestTimeCurrentBuild > finishTime:
            print("New Build Record: " + finishTimePretty)
            self.bestTimeCurrentBuild = finishTime
            self.bestTimeBuildLabel.setText(finishTimePretty)

        self.sessionRuns += 1
        self.daemon_heartbeat.start()

    def race_start_func(self):
        #if self.stage == STAGE_ID_TO_NAME[self.ridersObject.currentStage]:
            #self.retries = self.retries + 1
        #else:
            #self.retries = 0
        #self.retriesLabel.setText(str(self.retries))
        if self.sessionRuns != 0:
            self.reset_session()
        print("Race Start...")
        self.lastCheckedLap = 0
        self.lap1Label.setText("N/A")
        self.lap2Label.setText("N/A")
        self.lap3Label.setText("N/A")
        self.bestLap = -1
        self.bestLapLabel.setText("N/A")
        self.finishTimeLabel.setText("N/A")
        self.buddyDaemon.start()
        try:
            self.refresh_records()
        except:
            pass

    def reset_session(self):
        oldVals = [str(self.mode), str(self.character), str(self.stage), str(self.gear)]
        self.load_state()
        if oldVals != [self.mode, self.character, self.stage, self.gear]:
            self.bestLapTimeSession = -1
            self.bestSessionTime = -1
            self.bestSessionTimeLabel.setText('N/A')
            self.bestLapSessionLabel.setText('N/A')

    def lap_change_func(self,currLap,lastLap):
        centi = int(self.player.lapTimeList[lastLap-1])
        lapTime = ridersTime(centi)
        if lastLap > 0:
            print("Lap %2d:" % lastLap)
            print(lapTime.prettyTime)
            currLapLabel = getattr(self, f"lap{lastLap}Label")
            currLapLabel.setText(lapTime.prettyTime)
        #if this was the best or first completed lap
        if (centi < self.bestLap) or (self.bestLap == -1):
            self.bestLap = centi
            self.bestLapLabel.setText(lapTime.prettyTime)
        #if you beat the best lap time for the session
        if (centi < self.bestLapTimeSession) or (self.bestLapTimeSession == -1):
            self.bestLapTimeSession = centi
            self.bestLapSessionLabel.setText(ridersTime(centi).prettyTime)

        # TODO generalize this last bit so it can count 4+ laps in free race
        # probably need an override to check for the bitfield of total laps,
        # and also make sure it doesn't fuck with the entry class

        #if the current lap is greater than 4 (time trial end)
        if currLap >= 4: #this is fine if time trial mode is selected
            centiFinish = self.player.lastSplitLapTime
            finishTime = ridersTime(centiFinish)
            self.finishTimeLabel.setText(finishTime.prettyTime)

    #this function is meant to be an overwatch of the game state checking for passed laps
    #if it detects a lap change or game/player state, call a function specific for that.
    def buddy_daemon(self):
        currLap = int(self.player.currentLap)
        lastLap = int(self.lastCheckedLap) #despite the name 'lastLap' is the last passed lap in this function

        if self.ridersObject.exitMethod == ExitMethod.Retry or self.ridersObject.exitMethod == ExitMethod.Quit:
            self.daemon_heartbeat.start()
            self.buddyDaemon.stop()
            time.sleep(4)
            return

        if (currLap != lastLap) and (currLap > 1):
            self.lap_change_func(currLap,lastLap)
        self.lastCheckedLap = int(self.player.currentLap)

        if self.ridersObject.get_race_state() == RaceState.End:
            self.race_end_func()
            self.buddyDaemon.stop()
            self.daemon_heartbeat.start()




    # a second one to start/stop the daemon, based on the games current state
    def daemon_heartbeat_func(self):
        try:
            check_DME_hook()
            self.dmeLabel.setText("Hooked")
            if self.ridersObject.get_race_state() == RaceState.Countdown:
                print("Starting race....")
                self.load_state()
                self.race_start_func()
                self.daemon_heartbeat.stop()
        except AttributeError:
            self.load_state()
        except:
            pass
        if self.bestTimeStage == -1:
            try:
                self.refresh_records()
            except FileNotFoundError:
                print("TimeTable.csv not found")
                self.bestTimeStage = 0
            except:
                print("heartbeat refresh records failed")

    def refresh_records(self):
        try:
            self.recordsDf = pd.read_csv("TimeTable.csv")
            stageTimes = self.recordsDf[self.recordsDf['Stage'] == self.stage]
            stageTimes.sort_values(by=["Raw Final Time"], inplace=True)
            self.bestTimeStage = stageTimes['Raw Final Time'].iloc[0]
            self.bestTimeStageLabel.setText(stageTimes['Time'].iloc[0])
            if self.altBox.currentText() == "Best Race (Stage)":
                self.lap1AltLabel.setText(stageTimes['Lap 1'].iloc[0])
                self.lap2AltLabel.setText(stageTimes['Lap 2'].iloc[0])
                self.lap3AltLabel.setText(stageTimes['Lap 3'].iloc[0])
                self.finishTimeAltLabel.setText(stageTimes['Time'].iloc[0])
                self.bestLapAltLabel.setText(stageTimes['Best Lap Time'].iloc[0])
            try:
                buildTimes = stageTimes[(stageTimes["Character"] == self.character) & (stageTimes["Gear"] == self.gear)]
                self.bestTimeCurrentBuild = buildTimes['Raw Final Time'].iloc[0]
                self.bestTimeBuildLabel.setText(buildTimes['Time'].iloc[0])
                if self.altBox.currentText() == "Best Race (Build)":
                    self.lap1AltLabel.setText(buildTimes['Lap 1'].iloc[0])
                    self.lap2AltLabel.setText(buildTimes['Lap 2'].iloc[0])
                    self.lap3AltLabel.setText(buildTimes['Lap 3'].iloc[0])
                    self.finishTimeAltLabel.setText(buildTimes['Time'].iloc[0])
                    self.bestLapAltLabel.setText(buildTimes['Best Lap Time'].iloc[0])
            except:
                if self.altBox.currentText() == "Best Race (Build)":
                    self.lap1AltLabel.setText('N/A')
                    self.lap2AltLabel.setText('N/A')
                    self.lap3AltLabel.setText('N/A')
                    self.finishTimeAltLabel.setText('N/A')
                    self.bestLapAltLabel.setText('N/A')

        except FileNotFoundError:
            print("TimeTable.csv not found")
            self.bestTimeStage = 0
        except:
            if self.altBox.currentText() == "Best Race (Stage)":
                self.lap1AltLabel.setText('N/A')
                self.lap2AltLabel.setText('N/A')
                self.lap3AltLabel.setText('N/A')
                self.finishTimeAltLabel.setText('N/A')
                self.bestLapAltLabel.setText('N/A')





    def load_state(self):
        try:
            check_DME_hook()
            self.dmeLabel.setText("Hooked")
            self.player = get_player(0)
            self.ridersObject = RidersObject(object_overrides)
            if not self.buddyDaemon.isActive() and self.ridersObject.get_race_state() != RaceState.End:
                self.buddyDaemon.start()
                print("Daemon started")
            else:
                self.daemon_heartbeat.start()
            try:
                self.character = CHR_ID_TO_NAME[self.player.character]
            except KeyError:
                self.character = str(self.player.character)
            try:
                self.archetype = ARCH_ID_TO_NAME[self.player.characterArchetype]
            except KeyError:
                self.archetype = str(self.player.characterArchetype)
            try:
                self.gear = GEAR_ID_TO_NAME[self.player.extremeGear]
            except KeyError:
                self.gear = str(self.player.extremeGear)
            try:
                self.stage = STAGE_ID_TO_NAME[self.ridersObject.currentStage]
            except KeyError:
                self.stage = str(self.ridersObject.currentStage)
            try:
                self.mode = MODE_ID_TO_NAME[self.ridersObject.currentMode]
            except KeyError:
                self.mode = str(self.ridersObject.currentMode)
            try:
                self.type = type_lookup[self.player.typeAttributes]
            except KeyError as e:
                #print(e)
                self.type = str(self.player.typeAttributes)

            self.typeLabel.setText(self.type)
            self.archLabel.setText(self.archetype)
            self.charLabel.setText(self.character)
            self.gearLabel.setText(self.gear)
            self.stageLabel.setText(self.stage)
            self.modeLabel.setText(self.mode)
        except RuntimeError as e:
            # print(e)
            self.dmeLabel.setText("DME Status: Not hooked")
        except:
            pass
