from enum import Enum, unique

@unique
class ENUM_HitLocations(Enum):
    BACK = 0
    FRONT_RIGHT = 1
    FRONT_LEFT = 2
    SHOULDER_RIGHT = 3
    SHOULDER_LEFT = 4
    PHASER = 5
    NETWORKUNIT = 6

@unique
class ENUM_Weapon(Enum):
    PHASER = 0
    AUTORIFLE = 1
    SNIPER = 2
    BLASTER = 3
    BURSTRIFLE = 4
    SYSTEMHACK = 5
    RECHARGER = 6
    NANOVIRUS = 7
    RESTORE = 8
    SABOTAGE = 9
    FLAG = 10

@unique
class ENUM_Powerup(Enum):
    SPY = 0
    STEALTH = 1
    STATBOOST = 2
    INVULNERABILITY = 3
    DEFLECTORSHIELD = 4
    AMMO = 5
    INFINITEAMMO = 6
    SHIELDOVERLOAD = 7
    VIRUS = 8

@unique
class ENUM_NetworkUnitMode(Enum):
    EFFECTS = 0
    TARGET = 1
    POWERUPTERMINAL = 2
    FLAGSTATION = 3
    TERRITORY = 4
    RECHARGER = 5