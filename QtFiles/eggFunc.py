from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME

from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import *
import time

def check_DME_hook():
    if not DME.is_hooked():
        try:
            DME.hook()
        except RuntimeError as e:
            print(e)

def big_button_press():
    check_DME_hook()

    # Instantiate player ptr on py side
    player1 = Player(0, TE_PLAYER_PTR)

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

def get_player(port):
    player = Player(port, TE_PLAYER_PTR)
    return player

def setRings(ringCount: int,player):
    player.rings = ringCount

# def setBoostSpeed(boostSpeed,player):
#     player.gearStats[int(player.level)].boostSpeed = pSpeed(float(boostSpeed))
#
# def setBoostCost(boostCost,player):
#     player.gearStats[int(player.level)].boostCost = pSpeed(float(boostCost))
#
# def setTopSpeed(topSpeed,player):
#     player.gearStats[int(player.level)].topSpeed = pSpeed(float(topSpeed))
#
# def setDriftDashSpeed(dashSpeed,player):
#     player.gearStats[int(player.level)].driftDashSpeed = pSpeed(float(dashSpeed))
#
# def setDriftCost(driftCost,player):
#     player.gearStats[int(player.level)].driftCost = pSpeed(float(driftCost))
#
def setCurrentAir(air,player):
    player.currentAir = air
#
def playAnimation(ID,player):
    player.currentAnimationID = ID
