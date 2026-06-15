"""
CLASS SCHEMA FOR PLAYER
"""
import time

import dolphin_memory_engine as DME
from .include.Controller import Controller
from .include.GenericData import GenericData
from .include.GearStats import GearStats
from .include.Constants import *
from .GameState import GAME_VERSION

INIT_STATE = True

class Player:
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
    def __init__(self, playerNum, playerPtr=None):
        global INIT_STATE
        INIT_STATE = True
        # TODO: If TE, use the map file instead of this for ptr
        # If a player pointer is passed in, use that instead and skip the match.
        # This is especially helpful for when TE builds change pointers and the ptr hasn't been updated in the constants yet.
        if playerPtr:
            self.playerPtr = playerPtr + (0x1080 * playerNum)
        else:
            match GAME_VERSION:
                # Vanilla based IDs for vanilla, DX, FT
                case GameIDs.SONIC_RIDERS_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
                case GameIDs.SONIC_RIDERS_DX_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
                case GameIDs.SONIC_RIDERS_FT_ID:
                    self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)

                # TE is special, as the game is a shiftable dol.
                # I'd suggest using the map file to figure out what this is supposed to be,
                # Or having a user enter it manually if no map is passed in.
                case GameIDs.SONIC_RIDERS_TE_ID:
                    self.playerPtr = TE_PLAYER_PTR + (0x1080 * playerNum)

                # ZG has dynamic player ptrs, this is not very reliable as of now.
                case GameIDs.SONIC_RIDERS_ZG_ID:
                    self.playerPtr = ZG_PLAYER_PTR + (0x1120 * playerNum)
                case _:
                    pass
        pass
        # Inputs are always defined on game load, at least for P1.
        # The input ptr is always at the start of the playerPtr struct, so just read word from here and pass the struct ID
        ptr_start_addr = self.playerPtr

        # Go to pointer for controls, starts at offset 0
        self.input = Controller(DME.follow_pointers(ptr_start_addr, [0]), ptr)
        self.tornadoInvulnerabilityTimer = GenericData(ptr_start_addr + 0x4, u8)

        self.character = GenericData(ptr_start_addr + 0xBA, u8)
        self.extremeGear = GenericData(ptr_start_addr + 0xBB, u8)
        self.x = GenericData(ptr_start_addr + 0x1E4, f32)
        self.y = GenericData(ptr_start_addr + 0x1E8, f32)
        self.z = GenericData(ptr_start_addr + 0x1EC, f32)
        self.verticalRotation = GenericData(ptr_start_addr + 0x1F0, f32)
        self.horizontalRotation = GenericData(ptr_start_addr + 0x1F4, f32)
        self.rotationRoll = GenericData(ptr_start_addr + 0x1F8, f32)

        self.currentAnimationID = GenericData(ptr_start_addr + 0x764, u32)

        # GearStats[3] -> index per level
        self.gearStats = [GearStats(ptr_start_addr + 0x8DC, u32), GearStats(ptr_start_addr + 0x914, u32), GearStats(ptr_start_addr + 0x94C, u32)]
        self.currentAir = GenericData(ptr_start_addr + 0x984, u32)
        self.changeInAir_gain = GenericData(ptr_start_addr + 0x988, u32)
        self.changeInAir_loss = GenericData(ptr_start_addr + 0x98C, u32)

        self.speed = GenericData(ptr_start_addr + 0xAAC, f32)
        self.speedAsInt = GenericData(ptr_start_addr + 0xABC, u32)

        # Uses SpecialFlags enum
        self.specialFlags = GenericData(ptr_start_addr + 0x9D4, u32)

        # List of laps and their times in centiseconds, up to 99 laps
        self.lapTimeList = [GenericData(ptr_start_addr + x, u32) for x in range(0xBF4, 0xD7C, 0x4)]

        self.rings = GenericData(ptr_start_addr + 0xB98, u32)
        self.typeAttributes = GenericData(ptr_start_addr + 0xBD3, Flag("Type"))

        self.playerDisplayFlags = GenericData(ptr_start_addr + 0xBA8, u32)

        # Last recorded lap as an int, in centiseconds.
        self.lastSplitLapTime = GenericData(ptr_start_addr + 0xD80, u32)

        # This is an array of bytes:
        # 1st byte = ms, 2nd byte = sec, 3rd byte = min
        self.raceFinishTime = [GenericData(ptr_start_addr + 0xFF4, u8), GenericData(ptr_start_addr + 0xFF5, u8), GenericData(ptr_start_addr + 0xFF6, u8)]
        # Note: on lap being completed, this resets to zero in-game.
        self.lapElapsedTime = [GenericData(ptr_start_addr + 0xFF8, u8), GenericData(ptr_start_addr + 0xFF9, u8), GenericData(ptr_start_addr + 0xFFA, u8)]

        self.currentLap = GenericData(ptr_start_addr + 0x102A, u8)
        self.previousLap = GenericData(ptr_start_addr + 0x102B, u8)
        self.placement_counter = GenericData(ptr_start_addr + 0x102C, u8)
        self.placement = GenericData(ptr_start_addr + 0x102D, u8)
        self.level = GenericData(ptr_start_addr + 0x102E, u8)
        self.subState = GenericData(ptr_start_addr + 0x102F, u8)


        self.state = GenericData(ptr_start_addr + 0x1034, u8)
        self.previousState = GenericData(ptr_start_addr + 0x1034, u8)

        self.qteState = GenericData(ptr_start_addr + 0x1043, u8)
        self.unk1044 = GenericData(ptr_start_addr + 0x1044, u8)

        # TE SPECIFIC, all other builds check "archetype" with character checks instead
        self.characterArchetype = GenericData(ptr_start_addr + 0x107C, u8)

        # DO NOT TOUCH, REQUIRED FOR INIT/RUNTIME TO WORK
        INIT_STATE = False