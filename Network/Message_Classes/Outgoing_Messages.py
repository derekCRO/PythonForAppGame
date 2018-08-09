from random import randint

from Backend.Network.Message_Classes.Base_Classes import *


class REG_RESP(OutgoingMessage):
    def __init__(self, serialNum, netID, name):
        self.type = "REG_RESP"
        self.topicString = "QNET/REG/RESP"
        self.messageString = self.assemblePayload([serialNum, netID, name])

class SYSTEM_STATE(OutgoingMessage):
    def __init__(self, state):
        self.type = "SYSTEM_STATE"
        self.topicString = "QNET/SYSTEM/STATE"
        self.messageString = self.assemblePayload([state])

class SETTINGS_CORE(OutgoingMessage):
    def setup(self, gameName, gameType, gameTime, gameffMode, twoHands):
        self.type = "SETTINGS_CORE"
        self.topicString = "QNET/SETT/CORE"
        if(twoHands == True):
            twoHandsNum = 1
        else:
            twoHandsNum = 0
        self.messageString = self.assemblePayload([gameName, gameType, gameTime, gameffMode, twoHandsNum])

    def __init__(self, coreSettings):
        self.setup(coreSettings.name, coreSettings.type, coreSettings.time, coreSettings.friendlyFireMode, coreSettings.twoHandsEnabled)


class SETTINGS_CLASSIC(OutgoingMessage):
    def setup(self, mode, vipStatsNo, vipEliminationMode, vipsPerTeam, juggernautStatsNo, juggernautTransferMode, juggernautMaxTransfers, eliminatorLives):
        self.type = "SETTINGS_CLASSIC"
        self.topicString = "QNET/SETT/CLASSIC"
        vipElimMode = 1 if vipEliminationMode else 0
        self.messageString = self.assemblePayload(([mode, vipStatsNo, vipElimMode, vipsPerTeam, juggernautStatsNo, juggernautTransferMode, juggernautMaxTransfers, eliminatorLives]))

    def __init__(self, classicSettings):
        self.setup(classicSettings.gameMode, classicSettings.vipStatsNo, classicSettings.vipEliminationMode, classicSettings.vipsPerTeam, classicSettings.juggernautStatsNo, classicSettings.juggernautTransferMode, classicSettings.juggernautMaxTransfers, classicSettings.eliminatorLives)

class SETTINGS_CTF(OutgoingMessage):
    def setup(self, gameMode, flagCarrierStats, flagDropResetDelay, flagCapturedResetDelay, flagPass, defendingTeam):
        self.type = "SETTINGS_CTF"
        self.topicString = "QNET/SETT/CTF"
        flagPassMode = 1 if flagPass else 0
        self.messageString = self.assemblePayload([gameMode, flagCarrierStats, flagDropResetDelay, flagCapturedResetDelay, flagPassMode, defendingTeam])

    def __init__(self, ctfSettings):
        self.setup(ctfSettings.gameMode, ctfSettings.flagCarrierStats, ctfSettings.flagDropResetDelay, ctfSettings.flagCapturedResetDelay, ctfSettings.flagPass, ctfSettings.defendingTeam)

class SETTINGS_ZOMBIES(OutgoingMessage):
    def setup(self, teamsEnabled, hitOtherTeams):
        self.type = "SETTINGS_ZOMBIES"
        self.topicString = "QNET/SETT/ZOMBIES"
        self.messageString = self.assemblePayload([teamsEnabled, hitOtherTeams])

    def __init__(self, zombiesSettings):
        self.setup(zombiesSettings.teamsEnabled, zombiesSettings.hitOtherTeam)

class SETTINGS_TEAM1(OutgoingMessage):
    def setup(self, teamNo, red, green, blue, statsForTeam, idList):
        self.type = "SETTINGS_TEAM1"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/TEAM1/", teamNo)

        message = []
        message.append(red)
        message.append(green)
        message.append(blue)
        message.append(statsForTeam)
        for i in range(32):
            if(idList[i] == True):
                message.append(1)
            else:
                message.append(0)
        self.messageString = self.assemblePayload(message)

    def __init__(self, teamNo, team):
        self.setup(teamNo, team.red, team.green, team.blue, team.statsAssignment, team.getIDListForMessage())

class SETTINGS_TEAM2(OutgoingMessage):
    def setup(self, teamNo, idList):
        self.type = "SETTINGS_TEAM2"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/TEAM2/", teamNo)
        message = []
        for i in range(32):
            if(idList[32+i] == True):
                message.append(1)
            else:
                message.append(0)
        self.messageString = self.assemblePayload(message)

    def __init__(self, teamNo, team):
        self.setup(teamNo, team.getIDListForMessage())

class SETTINGS_WEAPON(OutgoingMessage):
    def setup(self, wpnNo, name, weaponType, fireRate, maxAmmo, mixedDamage, healthDamage, shieldDamage):
        self.type = "SETTINGS_WEAPON"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/WPNS/", wpnNo)
        self.messageString = self.assemblePayload([name, weaponType, fireRate, maxAmmo, mixedDamage, healthDamage, shieldDamage])

    def __init__(self, wpnNo, weapon):
        self.setup(wpnNo, weapon.name, weapon.type, weapon.fireRate, weapon.maxAmmo, weapon.mixedDamage, weapon.healthDamage, weapon.shieldDamage)

class SETTINGS_POWERUP(OutgoingMessage):
    def setup(self, powerupNo, name, type, maxCharges, variable1, variable2):
        self.type = "SETTINGS_POWERUP"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/PWRPS/", powerupNo)
        self.messageString = self.assemblePayload([name, type, maxCharges, variable1, variable2])

    def __init__(self, powerupNo, powerup):
        self.setup(powerupNo, powerup.name, powerup.type, powerup.maxCharges, powerup.variableOne, powerup.variableTwo)

class SETTINGS_STAT1(OutgoingMessage):
    def setup(self, statNo, maxHealth, maxshield, startingHealth, startingShield, healthRechargeRate, shieldRechargeRate, healthRechargeDelay, shieldRechargeDelay, tagBonusPowerup_3, tagBonusPowerup_5, tagBonusPowerup_7, tagBonusPowerup_10, defshields, warnings, reflex):
        self.type = "SETTINGS_STAT1"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/STAT1/", statNo)
        self.messageString = self.assemblePayload([maxHealth, maxshield, startingHealth, startingShield, healthRechargeRate, shieldRechargeRate, healthRechargeDelay, shieldRechargeDelay, tagBonusPowerup_3, tagBonusPowerup_5, tagBonusPowerup_7, tagBonusPowerup_10, defshields, warnings, reflex])

    def __init__(self, statNo, stat):
        self.setup(statNo, stat.maxHealth, stat.maxShield, stat.startingHealth, stat.startingShield, stat.healthRechargeRate, stat.shieldRechargeRate, stat.healthRechargeDelay, stat.shieldRechargeDelay, stat.tagBonusPowerup_3, stat.tagBonusPowerup_5, stat.tagBonusPowerup_7, stat.tagBonusPowerup_10, stat.defShields, stat.warnings, stat.reflex)

class SETTINGS_STAT2(OutgoingMessage):
    def setup(self, statNo, weaponList, powerupList):
        self.type = "SETTINGS_STAT2"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/STAT2/", statNo)
        statList = []
        for i in range(16):
            statList.append(weaponList[i])
        for i in range(16):
            statList.append(powerupList[i])
        self.messageString = self.assemblePayload(statList)

    def __init__(self, statNo, stat):
        self.setup(statNo, stat.weaponAmmo, stat.powerupAmmo)

class NETWORKUNIT_PROFILE(OutgoingMessage):
    def setup(self, profileNo, mode, outputMode, onboardLedsMode, soundMode, powerups, deactivationTime, flashTime, teamAffiliation, musicTrackNo):
        self.type = "NETWORKUNIT_PROFILE"
        self.topicString = self.assembleTopicWithSet("QNET/SETT/NET/", profileNo)
        parameters = []
        parameters.append(mode)
        for i in range(4):
            parameters.append(outputMode[i])
        parameters.append(onboardLedsMode)
        parameters.append(soundMode)
        for i in range(16):
            if(powerups[i] == True):
                parameters.append("1")
            else:
                parameters.append("0")
            #parameters.append(powerups[i])
        parameters.append(deactivationTime)
        parameters.append(flashTime)
        parameters.append(teamAffiliation)
        parameters.append(musicTrackNo)
        self.messageString = self.assemblePayload(parameters)

    def __init__(self, profileNo, profile):
        self.setup(profileNo, profile.mode, profile.outputMode, profile.onboardLedsMode, profile.soundMode, profile.powerups, profile.deactivationTime, profile.flashTime, profile.teamAffiliation, profile.musicTrackNo)

class NETWORKUNIT_ASSIGN(OutgoingMessage):
    def setup(self, idList):
        self.type = "NETWORKUNIT_ASSIGN"
        self.topicString = "QNET/SETT/NETASSIGN"
        self.messageString = self.assemblePayload(idList)

    def __init__(self, profiles):
        idList = []
        for i in range(32):
            teamForID = -1
            for j in range(8):
                if(profiles[j].ids[i] == True):
                    teamForID = j
                    break
            idList.append(teamForID)
        self.setup(idList)

"""
GAME STATE ENUMERATIONS
- Standby       0
- Setup         1
- Countdown     2
- Playing       3
- End           4
"""


class GAMESTATUS(OutgoingMessage):
    def setup(self, gamestate, gameID, timeSinceStart):
        self.type = "GAMESTATUS"
        self.topicString = "QNET/GAMESTATUS"
        self.messageString = self.assemblePayload([gamestate, gameID, timeSinceStart])

    def __init__(self, running, gameID, timeSinceStart):
        self.setup(running, gameID, timeSinceStart)

class SCOREUPDATE(OutgoingMessage):
    def setup(self, netID, playerScore, teamScore, playerScorePosition, teamScorePosition):
        self.type = "SCOREUPDATE"
        self.topicString = self.assembleTopicWithNetID("QNET/SCORE/", netID)
        self.messageString = self.assemblePayload([playerScore, teamScore, playerScorePosition, teamScorePosition])

    def __init__(self, netID, playerScore, teamScore, playerScorePosition, teamScorePosition):
        self.setup(netID, playerScore, teamScore, playerScorePosition, teamScorePosition)

class CCARD_ADD(OutgoingMessage):
    def setup(self, id, group):
        self.type = "CCARD_ADD"
        self.topicString = "QNET/CCARD/ADD"
        self.messageString = self.assemblePayload([id, group])

    def __init__(self, id, group):
        self.setup(id, group)

class CCARD_CLR(OutgoingMessage):
    def setup(self, group):
        self.type = "CCARD_CLR"
        self.topicString = "QNET/CCARD/CLR"
        self.messageString = self.assemblePayload([group])

    def __init__(self, group):
        self.setup(group)

class CCARD_LIST(OutgoingMessage):
    def setup(self, group, ids):
        self.type = "CCARD_LIST"
        self.topicString = self.assembleTopicWithSet("QNET/CCARD/LIST/", group)
        self.messageString = self.assemblePayload(ids)

    def __init__(self, group, ids):
        self.setup(group, ids)

class GAME_EVENT(OutgoingMessage):
    def setup(self, string):
        self.type = "GAME_EVENT"
        self.topicString = "QNET/GAME/EVENT"
        self.messageString = self.assemblePayload([string])

    def __init__(self, string):
        self.setup(string)

class EVENT_CLASSIC(OutgoingMessage):
    def setup(self, vips, juggernaut):
        self.type = "EVENT_CLASSIC"
        self.topicString = "QNET/EVENT/CLASSIC"
        newList = []
        for i in range(20):
            newList.append(vips[i])
        newList.append(juggernaut)
        self.messageString = self.assemblePayload(newList)

    def __init__(self, vips, juggernaut):
        self.setup(vips, juggernaut)

class EVENT_CTF(OutgoingMessage):
    def setup(self, carriers, cappedList, availableList):
        self.type = "EVENT_CTF"
        self.topicString = "QNET/EVENT/CTF"
        newList = []
        for i in range(8):
            newList.append(carriers[i])
        for i in range(8):
            newList.append(cappedList[i])
        for i in range(8):
            newList.append(1 if availableList[i] else 0)
        self.messageString = self.assemblePayload(newList)

    def __init__(self, carriers, cappedList, availableList):
        self.setup(carriers, cappedList, availableList)

class QCONFIGRSSI(OutgoingMessage):
    def setup(self, rssiString):
        self.type = "QCONFIGRSSI"
        self.topicString = "QCONFIGRSSI"
        self.messageString = rssiString

    def __init__(self, rssiString):
        self.setup(rssiString)