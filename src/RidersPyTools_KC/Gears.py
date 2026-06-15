from enum import IntFlag

GEAR_INVALID = 255
GEAR_DEFAULT = 0
GEAR_HIGH_BOOSTER = 1
GEAR_AUTO_SLIDER = 2
GEAR_POWERFUL = 3
GEAR_FASTEST = 4
GEAR_TURBO_STAR = 5
GEAR_SPEED_BALANCER = 6
GEAR_BLUE_STAR_II = 7
GEAR_ACCESS = 8
GEAR_BEGINNER = 9
GEAR_ACCELERATOR = 10
GEAR_TRAP = 11
GEAR_LIGHT_BOARD = 12
GEAR_SLIDE_BOOSTER = 13
GEAR_LEGEND = 14
GEAR_MAGIC_CARPET = 15
GEAR_AIR_BROOM = 16
GEAR_HOVERCRAFT = 17
GEAR_CHAOS_EMERALD = 18
GEAR_FASTER = 19
GEAR_GAMBLER = 20
GEAR_POWER = 21
GEAR_OPA_OPA = 22
GEAR_CRAZY = 23
GEAR_BERSERKER = 24
GEAR_E_RIDER = 25  # Eggman Default Gear (vanilla)
GEAR_AIR_TANK = 26
GEAR_HEAVY_BIKE = 27
GEAR_DESTROYER = 28
GEAR_OMNIPOTENCE = 29
GEAR_COVER_S = 30
GEAR_COVER_F = 31
GEAR_COVER_P = 32
GEAR_HANG_ON = 33
GEAR_SUPER_HANG_ON = 34
GEAR_DARKNESS = 35  # Shadow Default Gear (vanilla)
GEAR_GRINDER = 36
GEAR_ADVANTAGE_S = 37
GEAR_ADVANTAGE_F = 38
GEAR_ADVANTAGE_P = 39
GEAR_CANNONBALL = 40
GEAR_GUN_GEAR = 41 # TE Original No. 1
GEAR_BOARD_70 = 42 # TE Original No. 2
GEAR_BITO = 43 # TE Original No. 3


GEAR_ID_TO_NAME = {
    GEAR_INVALID: "", # This should show nothing
    GEAR_DEFAULT: "Default Gear",
    GEAR_HIGH_BOOSTER: "High Booster",
    GEAR_AUTO_SLIDER: "Auto Slider",
    GEAR_POWERFUL: "Powerful Gear",
    GEAR_FASTEST: "Fastest",
    GEAR_TURBO_STAR: "Turbo Star",
    GEAR_SPEED_BALANCER: "Speed Balancer",
    GEAR_BLUE_STAR_II: "Blue Star II",
    GEAR_ACCESS: "Access",
    GEAR_BEGINNER: "Beginner",
    GEAR_ACCELERATOR: "Accelerator",
    GEAR_TRAP: "Trap Gear",
    GEAR_LIGHT_BOARD: "Light Board",
    GEAR_SLIDE_BOOSTER: "Slide Booster",
    GEAR_LEGEND: "Legend",
    GEAR_MAGIC_CARPET: "Magic Carpet",
    GEAR_AIR_BROOM: "Air Broom",
    GEAR_HOVERCRAFT: "Hovercraft",
    GEAR_CHAOS_EMERALD: "Chaos Emeralds",
    GEAR_FASTER: "Faster",
    GEAR_GAMBLER: "Gambler",
    GEAR_POWER: "Power Gear",
    GEAR_OPA_OPA: "Opa Opa",
    GEAR_CRAZY: "The Crazy",
    GEAR_BERSERKER: "Berserker",
    GEAR_E_RIDER: "E-Rider",
    GEAR_AIR_TANK: "Air Tank",
    GEAR_HEAVY_BIKE: "Heavy Bike",
    GEAR_DESTROYER: "Destroyer",
    GEAR_OMNIPOTENCE: "Omnipotence",
    GEAR_COVER_S: "Cover-S",
    GEAR_COVER_F: "Cover-F",
    GEAR_COVER_P: "Cover-P",
    GEAR_HANG_ON: "Hang-On",
    GEAR_SUPER_HANG_ON: "Super Hang-On",
    GEAR_DARKNESS: "Darkness",
    GEAR_GRINDER: "Grinder",
    GEAR_ADVANTAGE_S: "Advantage-S",
    GEAR_ADVANTAGE_F: "Advantage-F",
    GEAR_ADVANTAGE_P: "Advantage-P",
    GEAR_CANNONBALL: "Cannonball",
    GEAR_GUN_GEAR: "Gun Gear",
    GEAR_BOARD_70: "Board '70",
    GEAR_BITO: "Bito"
}
ALL_GEARS = list(GEAR_ID_TO_NAME.keys())

# Based off TE's version.
# DX unfortunately has reworked some of them, so their behavior may be unknown. Sorry.
class SpecialFlags(IntFlag):
	noSpecialFlags              = 0,
	alwaysIgnoreTurbulence      = 1 << 0,
	legendEffect 				= 1 << 1,
	alwaysOnIce 				= 1 << 2,
	unk 						= 1 << 3,
	noBoosting 					= 1 << 4,
	autoDrift 					= 1 << 5,
	noSpeedLossUphill 			= 1 << 6,
	tornadoBoost 				= 1 << 7,
	noSpeedLossChargingJump 	= 1 << 8,
	firstPlaceDoubleRings 		= 1 << 9,
	ringGear 					= 1 << 10,
	disableAttacks 				= 1 << 11,
	berserkerEffect 			= 1 << 12,
	noTypeShortcuts 			= 1 << 13,
	noPits 						= 1 << 14,
	thirtyPercentAir 			= 1 << 15,
	fiftyPercentAir 			= 1 << 16,
	iceImmunity 				= 1 << 17,
	lightBoardEffect 			= 1 << 18,
	stickyFingers 				= 1 << 19,
	# custom
	lowBoost 					= 1 << 20,
	lowerDecel 					= 1 << 21,
	noBoostChain 				= 1 << 22,
	noSpeedLossTurning 			= 1 << 23,
	ignoreOffroad    			= 1 << 24,
	moneyCrisis					= 1 << 25,
	noBoostSpeedBoostChain		= 1 << 26