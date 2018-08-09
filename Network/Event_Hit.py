from .Enumerations import *

class Event_Hit():
    def __init__(self, gameSettings, shooterID, targetID, weaponID, hitLocation, targetHealth, targetShield, flags, vipsList, juggernaut, flagCarriers):
        self.gameSettings = gameSettings
        self.shooterID = shooterID
        self.targetID = targetID
        self.weaponID = weaponID
        self.hitLocation = hitLocation
        self.targetHealth = targetHealth
        self.targetShield = targetShield
        self.flags = flags
        self.vipsList = vipsList
        self.juggernaut = juggernaut
        self.flagCarriers = flagCarriers

    def isValid(self):
        return (self.shooterID >= 0 and self.shooterID <= 95
                and (self.targetID >= 0 and self.targetID <= 95)        #valid ID
                and ((self.weaponID >= 0 and self.weaponID <= 15) or (self.shooterID >= 64 and self.shooterID <= 95 and self.weaponID == 255))  #valid weapon
                and (self.hitLocation <= 6)                             #valid hit location
                and (self.getShooterTeam() != -1 or self.shooterIsNetworkUnit())            #valid shooter team
                and (self.getTargetTeam() != -1 or self.targetIsNetworkUnit())              #valid target team
                and (self.getShooterNetworkUnitProfile() != -1)
                and (self.getTargetNetworkUnitProfile() != -1)
                )

    def shooterIsNetworkUnit(self):
        return (self.shooterID >= 64 and self.shooterID <= 95)

    def shooterIsPhaser(self):
        return (self.shooterID <= 63 and self.shooterID >= 0)

    def targetIsNetworkUnit(self):
        return (self.targetID >= 64 and self.targetID <= 95)

    def targetIsPhaser(self):
        return (self.targetID <= 63 and self.targetID >= 0)

    def getShooterNetworkUnitProfile(self):
        if(not self.shooterIsNetworkUnit()):
            return -2
        profileNum = self.gameSettings.findNetworkUnitProfile(self.shooterID)
        if (profileNum == -1):
            return -1
        return self.gameSettings.networkUnitProfiles[profileNum]

    def getShooterNetworkUnitProfileMode(self):
        profile = self.getShooterNetworkUnitProfile()
        if(profile == -1 or profile == -2):
            return -1
        return ENUM_NetworkUnitMode(profile.mode).name

    def getTargetNetworkUnitProfile(self):
        if(not self.targetIsNetworkUnit()):
            return -2
        profileNum = self.gameSettings.findNetworkUnitProfile(self.targetID)
        if(profileNum == -1):
            return -1
        return self.gameSettings.networkUnitProfiles[profileNum]

    def getTargetNetworkUnitProfileMode(self):
        profile = self.getTargetNetworkUnitProfile()
        if(profile == -1 or profile == -2):
            return -1
        return ENUM_NetworkUnitMode(profile.mode).name

    def getShooterTeam(self):
        if(self.shooterIsPhaser()):
            return self.gameSettings.findTeam(self.shooterID)
        else:
            return self.getShooterNetworkUnitProfile().teamAffiliation

    def getTargetTeam(self):
        if(self.targetIsPhaser()):
            return self.gameSettings.findTeam(self.targetID)
        else:
            return self.getTargetNetworkUnitProfile().teamAffiliation

    def getHitLocation(self):
        return ENUM_HitLocations(self.hitLocation).name

    def getWeaponType(self):
        return ENUM_Weapon(self.gameSettings.weapons[self.weaponID].type).name

    def wasEliminated(self):
        return (self.targetHealth == 0)

    def shooterWasVIP(self):
        return self.shooterID in self.vipsList

    def targetWasVIP(self):
        return self.targetID in self.vipsList

    def shooterWasJuggernaut(self):
        return self.shooterID == self.juggernaut

    def targetWasJuggernaut(self):
        return self.targetID == self.juggernaut

    def shooterHasFlag(self):
        return self.shooterID in self.flagCarriers

    def targetHasFlag(self):
        return self.targetID in self.flagCarriers

    def wasFriendlyFire(self):
        return self.getTargetTeam() == self.getShooterTeam()

    def getWeapon(self):
        return self.gameSettings.weapons[self.weaponID]

    def getPowerupHitFlag(self):
        if(self.flags != -1 and self.flags <= 15 and self.flags >= 0):
            return ENUM_Powerup(self.gameSettings.powerups[self.flags].type).name
        else:
            return -1