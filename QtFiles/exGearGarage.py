from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from eggFunc import *

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

class eggWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("exGearGarage.ui", self)
        self.setWindowTitle("E.G.G. - Extreme Gear Garage")
        #self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))
        self.setWindowIcon(QtGui.QIcon("jordskatoolIcon.png"))
        self.maxLevel = 3
        self.playerNum = 1
        self.portSpinBox.valueChanged.connect(self.change_port)

        self.BBButton.clicked.connect(big_button_press)
        self.ring0Button.clicked.connect(lambda checked=False: self.ringSetter(0))
        self.ring30Button.clicked.connect(lambda checked=False: self.ringSetter(30))
        self.ring60Button.clicked.connect(lambda checked=False: self.ringSetter(60))
        self.playAnimButton.clicked.connect(self.egg_animation_clicked)
        self.setValButton.clicked.connect(self.set_all_val_clicked)
        self.airSlider.sliderMoved.connect(self.setCurrentAirFromSlider)
        self.setMaxAirButton.clicked.connect(lambda checked=False: self.airSetter(100))
        self.set0AirButton.clicked.connect(lambda checked=False: self.airSetter(0))
        self.ringsBox.valueChanged.connect(self.ringSetter)
        #Timers
        #daemon to prevent crashing if DME isn't hooked
        self.eggDaemon = QtCore.QTimer()
        self.eggDaemon.setInterval(500)
        self.eggDaemon.timeout.connect(self.egg_daemon)
        self.eggDaemon.start()
        #fast for updating rings/air
        self.fastEggTimer = QtCore.QTimer()
        self.fastEggTimer.setInterval(100)
        self.fastEggTimer.timeout.connect(self.egg_fast_update)
        #self.fastEggTimer.start()
        #slow for updating gear stats
        self.slowEggTimer = QtCore.QTimer()
        self.slowEggTimer.setInterval(1000)
        self.slowEggTimer.timeout.connect(self.egg_slow_update)
        #self.slowEggTimer.start()
        #slower for updating game+player
        self.chrEggTimer = QtCore.QTimer()
        self.chrEggTimer.setInterval(1500)
        self.chrEggTimer.timeout.connect(self.egg_char_update)
        #self.chrTimer.start()

        #checkbox to pause timer for updating values
        self.timerPauseChkbx.checkStateChanged.connect(self.pause_egg_timer)

        for i in range(1,self.maxLevel+1):
            boostSpeedBox = getattr(self, f"setBoostSpeedSpinBox_{i}")
            boostCostBox = getattr(self, f"setBoostCostSpinBox_{i}")
            topSpeedBox = getattr(self, f"setTopSpeedSpinBox_{i}")
            driftDashSpeedBox = getattr(self, f"setDriftDashSpeedSpinBox_{i}")
            driftCostBox = getattr(self, f"setDriftCostSpinBox_{i}")

            boostSpeedBox.editingFinished.connect(self.set_all_val_clicked)
            boostCostBox.editingFinished.connect(self.set_all_val_clicked)
            topSpeedBox.editingFinished.connect(self.set_all_val_clicked)
            driftDashSpeedBox.editingFinished.connect(self.set_all_val_clicked)
            driftCostBox.editingFinished.connect(self.set_all_val_clicked)



    # FUNCTIONS
    def change_port(self,value):
        self.playerNum = value
        self.egg_fast_update()

    def egg_animation_clicked(self):
        playAnimation(self.animIDSpinBox.value(), self.player)

    def airSetter(self, value):
        maxAir = self.player.gearStats[int(self.player.level)].maxAir
        air = (value / 100) * maxAir
        setCurrentAir(air,self.player)

    def ringSetter(self, value):
        setRings(value,self.player)


    def set_all_val_clicked(self):
        for i in range(1,self.maxLevel+1):
            boostSpeedBox = getattr(self, f"setBoostSpeedSpinBox_{i}")
            boostCostBox = getattr(self, f"setBoostCostSpinBox_{i}")
            topSpeedBox = getattr(self, f"setTopSpeedSpinBox_{i}")
            driftDashSpeedBox = getattr(self, f"setDriftDashSpeedSpinBox_{i}")
            driftCostBox = getattr(self, f"setDriftCostSpinBox_{i}")

            self.player.gearStats[int(i-1)].boostSpeed = pSpeed(float(boostSpeedBox.value()))
            self.player.gearStats[int(i-1)].boostCost = float(boostCostBox.value())
            self.player.gearStats[int(i-1)].topSpeed = pSpeed(float(topSpeedBox.value()))
            self.player.gearStats[int(i-1)].driftDashSpeed = pSpeed(float(driftDashSpeedBox.value()))
            self.player.gearStats[int(i-1)].driftCost = float(driftCostBox.value())

    def setCurrentAirFromSlider(self):
        maxAir = self.player.gearStats[int(self.player.level)].maxAir
        air = (self.airSlider.value()/100) * maxAir
        setCurrentAir(air,self.player)


    def pause_egg_timer(self):
        if self.timerPauseChkbx.isChecked():
            self.slowEggTimer.stop()
        else:
            self.slowEggTimer.start()

    def egg_daemon(self):
        if not DME.is_hooked():
            try:
                DME.hook()
                if DME.is_hooked():
                    self.dmeLabel.setText("Hooked")
                    self.fastEggTimer.start()
                    self.slowEggTimer.start()
                    self.chrEggTimer.start()
                else:
                    raise RuntimeError("DME Hook failed")
            except RuntimeError as e:
                print(e)
                self.dmeLabel.setText("Not hooked")
        elif DME.is_hooked():
            self.egg_char_update()
            if not self.fastEggTimer.isActive():
                self.fastEggTimer.start()
            if not self.slowEggTimer.isActive():
                self.slowEggTimer.start()
            if not self.chrEggTimer.isActive():
                self.chrEggTimer.isActive()

    def egg_fast_update(self):
        try:
            currentRings = int(self.player.rings)
            maxAir = self.player.gearStats[int(self.player.level)].maxAir
            currentAir = self.player.currentAir

            new_value = (int(currentAir) / int(maxAir))
            bar_value = int(new_value * 100)

            self.ringsBox.setValue(currentRings)
            self.airSlider.setValue(bar_value)
        except:
            pass

    def egg_slow_update(self):
        try:
            currentLevel = int(self.player.level +1)
            self.currLevelLabel.setText("Current Level: %d" % currentLevel)

            for i in range(1,self.maxLevel+1):
                stats = self.player.gearStats[i -1]
                boostSpeedBox = getattr(self, f"setBoostSpeedSpinBox_{i}")
                boostCostBox = getattr(self, f"setBoostCostSpinBox_{i}")
                topSpeedBox = getattr(self, f"setTopSpeedSpinBox_{i}")
                driftDashSpeedBox = getattr(self, f"setDriftDashSpeedSpinBox_{i}")
                driftCostBox = getattr(self, f"setDriftCostSpinBox_{i}")

                boostSpeedBox.setValue(int(round(stats.boostSpeed * SPEED_DIVISOR)))
                boostCostBox.setValue(int(stats.boostCost))
                topSpeedBox.setValue(int(round(stats.topSpeed * SPEED_DIVISOR)))
                driftDashSpeedBox.setValue(int(round(stats.driftDashSpeed * SPEED_DIVISOR)))
                driftCostBox.setValue(int(stats.driftCost))
        except:
            pass

    def egg_char_update(self):
        try:
            self.dmeLabel.setText("DME Status: Hooked")
            self.player = get_player(self.playerNum - 1)
            self.ridersObject = RidersObject(object_overrides)

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

            self.archLabel.setText("Archetype: "+self.archetype)
            self.charLabel.setText("Character: "+self.character)
            self.gearLabel.setText("Gear: "+self.gear)
            self.stageLabel.setText("Stage: "+self.stage)
        except RuntimeError as e:
            print(e)
            self.dmeLabel.setText("DME Status: Not hooked")
