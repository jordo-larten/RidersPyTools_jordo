"""
Contains all memory addresses from map/vanilla addresses fallback
"""

import dolphin_memory_engine as DME
from .include.Controller import Controller
from .include.GenericData import GenericData
from .include.GearStats import GearStats
from .include.Constants import *
from .GameState import GAME_VERSION, RACESTATE_ID_TO_NAME, ALL_RACESTATES, RaceState
from .Player import Player

INIT_STATE = True

# Note: these are vanilla addresses as default
default_general_addresses = {
    "gameID": 0x80000000,
    "CurrentGameMode": 0x806129A0,
    "geGame_ModeDetail": 0x806129A4,
    "CurrentStage": 0x806129A8,
    "RaceExitMethod": 0x806129C0,
    "StageTimer": 0x80612B40,
}


buildDir = load_path()
if buildDir:
    lookingList = ["CurrentGameMode", "geGame_ModeDetail", "CurrentStage", "RaceExitMethod"]
    ptr_dict_list = read_for_list(buildDir, lookingList)
    for key,value in ptr_dict_list.items():
        default_general_addresses[key] = value


class RidersObject:
    def __getattr__(self, name):
        global INIT_STATE

        if INIT_STATE:
            return None

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = vars(self.__getattribute__(name))["_datatype"]
        offset_to_read = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        if 'READ_FROM_DME' in name:
            try:
                value_read = None
                if type_to_read == u8 or type_to_read == s8 or type_to_read == Bool:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u16 or type_to_read == s16:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u32 or type_to_read == s32 or type_to_read == vu32:
                    value_read = DME.read_word(offset_to_read)
                if type_to_read == f32:
                    value_read = DME.read_float(offset_to_read)
                if value_read is None:
                    # No types were valid, read bytes instead
                    value_read = DME.read_bytes(offset_to_read, type_to_read)
                return value_read
            except RuntimeError as e:
                print("RuntimeError: DME is " + str(e) + ". Failed to return value.")
        return vars(self.__getattribute__(name))
    def __setattr__(self, name, value):
        global INIT_STATE

        # On startup, this allows everything to be assigned to the player object.
        # We NEED this for init ONLY.
        # Once every struct variable is done, SET INIT_STATE = False.
        # Once that is done, this will retrieve data from DME instead of setting the attribute's value.
        if INIT_STATE:
            super().__setattr__(name, value)
            return
        # Use this function for GenericData value assignment that isn't setting equal to a new object instance (that's handled in their own classes)

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        # check_DME_value = vars(self.__getattribute__(name))
        type_to_write = vars(self.__getattribute__(name))["_datatype"]
        offset_to_write = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        try:
            if type_to_write == u8 or type_to_write == s8 or type_to_write == Bool:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u16 or type_to_write == s16:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u32 or type_to_write == s32 or type_to_write == vu32:
                DME.write_word(offset_to_write, value)
            if type_to_write == f32:
                DME.write_float(offset_to_write, value)
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to write new value.")
        return
    def __init__(self, replacement_values: dict = None):
        global INIT_STATE
        INIT_STATE = True
        # Find a way to define literally EVERY SYMBOL here.
        # Not easy, but most are defined. Some are custom with pointers and structs. Good luck.

        # This is a hack that allows me to change where the addresses are.
        # This makes it easier to find while we're testing TE.
        # If no address found, use vanilla.
        # If you want this for TE, send in stageTimerAddr 0x8053C480
        # TE 2.4.6.1 currentStageAddr 0x8053C2E8

        addresses_to_use = default_general_addresses | replacement_values

        # This is 6 bytes long.
        self.gameID = GenericData(addresses_to_use["gameID"], 0x6)

        self.currentMode = GenericData(addresses_to_use["CurrentGameMode"], vu32)
        self.gameModeDetail = GenericData(addresses_to_use["geGame_ModeDetail"], vu32)
        self.currentStage = GenericData(addresses_to_use["CurrentStage"], vu32)
        self.exitMethod = GenericData(addresses_to_use["RaceExitMethod"], u32)
        self.stageTimer = [GenericData(addresses_to_use["StageTimer"], u8),
                           GenericData(addresses_to_use["StageTimer"] + 0x1, u8),
                           GenericData(addresses_to_use["StageTimer"] + 0x2, u8)]

        # List of all players 1-4
        self.players = [Player(0 + idx) for idx in range(0, 3)]

        INIT_STATE = False
        pass

    def get_race_state(self, return_text=False):
        if return_text:
            return RACESTATE_ID_TO_NAME[RaceState(self.gameModeDetail - self.currentMode)]
        return RaceState(self.gameModeDetail - self.currentMode)

    def get_current_race_time(self):
        minutes = (self.stageTimer[2])
        seconds = (self.stageTimer[1])
        milliseconds = (self.stageTimer[0])
        return "{:02d}:{:02d}:{:02d}".format(minutes, seconds, milliseconds)
