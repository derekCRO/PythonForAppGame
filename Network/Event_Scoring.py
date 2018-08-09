from .Event_Hit import *

"""
class Event_Scoring():
    def __init__(self, hitEvent, vipList, juggernaut, flagCarriers):
        self.hitEvent = hitEvent
        self.vipList = vipList
        self.juggernaut = juggernaut
        self.flagCarriers = flagCarriers
"""

class Event_Score_Player():
    def __init__(self, player, scoreChange):
        self.player = player
        self.scoreChange = scoreChange

class Event_Score_Team():
    def __init__(self, team, scoreChange):
        self.team = team
        self.scoreChange = scoreChange

class Event_Score_Player_Stat():
    def __init__(self, player, statKey, change):
        self.player = player
        self.statKey = statKey
        self.statChange = change

class Event_Score_Generic():
    def __init__(self):
        self.ScoringEvents = []




"""
GENERAL SCORE EVENTS
"""

class Event_Score_General_Player_Tagged_Player(Event_Score_Generic):
    def __init__(self, hitEvent):
        Event_Score_Generic.__init__(self)
        self.ScoringEvents.append(Event_Score_Player(hitEvent.shooterID, hitEvent.gameSettings.playerScoring.hitOpponent))
        self.ScoringEvents.append(Event_Score_Player(hitEvent.targetID, hitEvent.gameSettings.playerScoring.hitByOpponent))
        self.ScoringEvents.append(Event_Score_Team(hitEvent.getShooterTeam(), hitEvent.gameSettings.teamScoring.hitOpponent))
        self.ScoringEvents.append(Event_Score_Team(hitEvent.getTargetTeam(), hitEvent.gameSettings.teamScoring.hitByOpponent))
        self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'PLAYERS_TAGGED', 1))
        self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.targetID, 'TIMES_TAGGED', 1))

        weaponType = hitEvent.getWeaponType()
        if(weaponType == ENUM_Weapon.PHASER):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_STANDARD', 1))
        elif(weaponType == ENUM_Weapon.AUTORIFLE):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_AUTORIFLE', 1))
        elif (weaponType == ENUM_Weapon.SNIPER):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_SNIPER', 1))
        elif (weaponType == ENUM_Weapon.BLASTER):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_BLASTER', 1))
        elif (weaponType == ENUM_Weapon.BURSTRIFLE):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_BURSTRIFLE', 1))
        elif (weaponType == ENUM_Weapon.SYSTEMHACK):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_SYSTEMHACK', 1))
        elif (weaponType == ENUM_Weapon.RECHARGER):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_RECHARGER', 1))
        elif (weaponType == ENUM_Weapon.NANOVIRUS):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_NANOVIRUS', 1))
        elif (weaponType == ENUM_Weapon.RESTORE):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_RESTORE', 1))
        elif (weaponType == ENUM_Weapon.SABOTAGE):
            self.ScoringEvents.append(Event_Score_Player_Stat(hitEvent.shooterID, 'WPN_SABOTAGE', 1))

"""
GAME SPECIFIC EVENTS
"""
class Event_Score_CTF_FlagCapture(Event_Score_Generic):
    def __init__(self, player, settings):
        Event_Score_Generic.__init__(self)
        self.ScoringEvents.append(Event_Score_Player(player, settings.playerScoring.capturedFlag))
        self.ScoringEvents.append(Event_Score_Team(settings.findTeam(player), settings.teamScoring.capturedFlag))
        self.ScoringEvents.append(Event_Score_Player_Stat(player, 'FLAG_CAPTURED', 1))

class Event_Score_CTF_HitFlagCarrier(Event_Score_Generic):
    def __init__(self, player, settings):
        Event_Score_Generic.__init__(self)
        self.ScoringEvents.append(Event_Score_Player(player, settings.playerScoring.hitFlagCarrier))
        self.ScoringEvents.append(Event_Score_Team(settings.findTeam(player), settings.teamScoring.hitFlagCarrier))

class Event_Score_CTF_TookFlag(Event_Score_Generic):
    def __init__(self, player, settings):
        Event_Score_Generic.__init__(self)
        self.ScoringEvents.append(Event_Score_Player(player, settings.playerScoring.tookFlag))
        self.ScoringEvents.append(Event_Score_Team(settings.findTeam(player), settings.teamScoring.tookFlag))