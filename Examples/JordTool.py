import tkinter as tk
from tkinter import ttk

from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import RidersObject
from src.RidersPyTools_KC.include.Constants import *
import time
import datetime

def big_button_press():
    # Instantiate player ptr on py side
    #player1 = Player(0, TE_PLAYER_PTR)

    # Test get values
    try:
        print("Character:", CHR_ID_TO_NAME[int(player1.character)])
    except KeyError:
        print("Character ID:", int(player1.character))

    try:
        print("Extreme Gear:", GEAR_ID_TO_NAME[int(player1.extremeGear)])
    except KeyError:
        print("Extreme Gear ID:", int(player1.extremeGear))

    try:
        print("Character archetype:", ARCH_ID_TO_NAME[int(player1.characterArchetype)])
    except KeyError:
        print("Character archetype ID:", int(player1.characterArchetype))

    print("Current lap:", player1.currentLap)
    print("Player State:", player1.state)

    # Let's adjust their rings!
    print("Changing rings.")
    print("Rings before change:", player1.rings)

    # Set the ring value on the player
    player1.rings = 100
    print("Rings after change:", player1.rings)

    # Play an animation for fun!
    player1.currentAnimationID = 62

    # Do a pause for a second since scripting does not frame match dolphin
    time.sleep(0.05)

    # Set boost speed
    player1.gearStats[int(player1.level)].boostSpeed = pSpeed(300.0)

def setRings(ringCount):
    player1.rings = ringCount

def setBoostSpeed():
    boostSpeed = float(boostSpeedSetVal.get())
    player1.gearStats[int(player1.level)].boostSpeed = pSpeed(float(boostSpeed))

def setBoostCost():
    boostCost = float(boostCostSetVal.get())
    player1.gearStats[int(player1.level)].boostCost = pSpeed(float(boostCost))

def setTopSpeed():
    topSpeed = float(topSpeedSetVal.get())
    player1.gearStats[int(player1.level)].topSpeed = pSpeed(float(topSpeed))

def setDriftDashSpeed():
    driftDashSpeed = float(topSpeedSetVal.get())
    player1.gearStats[int(player1.level)].driftDashSpeed = pSpeed(float(driftDashSpeed))

def setDriftCost():
    driftCost = float(topSpeedSetVal.get())
    player1.gearStats[int(player1.level)].driftCost = pSpeed(float(driftCost))


DME.hook()
player1 = Player(0, TE_PLAYER_PTR)

root = tk.Tk()

root.title("JordTool")

window_width = 300
window_height = 200

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

ttk.Button(root, text="Big Button",command=big_button_press).pack()
ttk.Button(root, text="Level 1 Rings",command=lambda: setRings(0)).pack()
ttk.Button(root, text="Level 2 Rings",command=lambda: setRings(30)).pack()
ttk.Button(root, text="Level 3 Rings",command=lambda: setRings(60)).pack()
#boostspeed
#boostcost
#topspeed
#ddashspeed
#dcost

boostSpeedSetVal = tk.StringVar()
boostSpeedSetVal_ = ttk.Entry(root, textvariable=boostSpeedSetVal).pack()
ttk.Button(root, text="Set Boost Speed",command=lambda: setBoostSpeed()).pack()

boostCostSetVal = tk.StringVar()
boostCostSetVal_ = ttk.Entry(root, textvariable=boostCostSetVal).pack()
ttk.Button(root, text="Set Boost Cost",command=lambda: setBoostCost()).pack()

topSpeedSetVal = tk.StringVar()
topSpeedSetVal_ = ttk.Entry(root, textvariable=topSpeedSetVal).pack()
ttk.Button(root, text="Set Top Speed",command=lambda: setTopSpeed()).pack()

driftDashSpeedSetVal = tk.StringVar()
driftDashSpeedSetVal_ = ttk.Entry(root, textvariable=driftDashSpeedSetVal).pack()
ttk.Button(root, text="Set Drift Dash Speed",command=lambda: setDriftDashSpeed()).pack()

driftCostSetVal = tk.StringVar()
driftCostVal_ = ttk.Entry(root, textvariable=driftCostSetVal).pack()
ttk.Button(root, text="Set Drift Cost",command=lambda: setDriftCost()).pack()

"""
driftFramesVal = tk.StringVar()
driftFramesVal_ = ttk.Entry(root, textvariable=driftFramesVal).pack()
ttk.Button(root, text="Set Boost Speed",command=lambda: setBoostSpeed()).pack()
"""
#should be at end always
root.mainloop()