from .Gametypes import *
from .Settings_Classes import *

#this class is used to run games
class GameSettings():
    def __init__(self):
        self.IDname = "Unnamed"
        self.coreSettings = Core_Settings()
        self.classicSettings = Game_Classic()
        self.ctfSettings = Game_CTF()
        self.territoriesSettings = Game_Territories()
        self.zombiesSettings = Game_Zombies()

        self.teams = [Team() for _ in range(8)]
        self.stats = [Stats() for _ in range(8)]
        self.networkUnitProfiles = [NetworkUnitProfile() for _ in range(8)]
        self.powerups = [Powerup() for _ in range(16)]
        self.weapons = [Weapon() for _ in range(16)]
        self.teamScoring = Scoring(True)
        self.playerScoring = Scoring(False)

    def findNetworkUnitProfile(self, netID):
        for i in range(len(self.networkUnitProfiles)):
            if(self.networkUnitProfiles[i].isDeviceInProfile(netID)):
                return i
        return -1

    def findTeam(self, netID):
        if(netID >= 64):
            return -1
        for i in range(len(self.teams)):
            if(self.teams[i].isPlayerInTeam(netID)):
                return i
        return -1


#this class is used for saving and loading presets. Just assign numbers on most.
class Game_Settings_Data():

    #in this format for jsonpickle to be backward compatible
    IDname = "Unnamed"
    coreSettings = Core_Settings()
    classicSettings = Game_Classic()
    ctfSettings = Game_CTF()
    territoriesSettings = Game_Territories()
    zombiesSettings = Game_Zombies()
    teams = [Team() for _ in range(8)]
    teamScoring = Scoring(True)
    playerScoring = Scoring(False)
    stats = [Stats() for _ in range(8)]
    weapons = [Weapon() for _ in range(16)]
    powerups = [Powerup() for _ in range(16)]
    networkUnitProfiles = [NetworkUnitProfile() for _ in range(8)]
    def __init__(self):

        #this format so that new instantiations are initialised correctly
        self.IDname = "Unnamed"
        self.coreSettings = Core_Settings()
        self.classicSettings = Game_Classic()
        self.ctfSettings = Game_CTF()
        self.territoriesSettings = Game_Territories()
        self.zombiesSettings = Game_Zombies()
        self.teams = [Team() for _ in range(8)]
        self.teamScoring = Scoring(True)
        self.playerScoring = Scoring(False)
        self.stats = [Stats() for _ in range(8)]
        self.weapons = [Weapon() for _ in range(16)]
        self.powerups = [Powerup() for _ in range(16)]
        self.networkUnitProfiles = [NetworkUnitProfile() for _ in range(8)]
        """
        self.IDname = "Unnamed"
        self.coreSettings = Core_Settings()
        self.classicSettings = Game_Classic()
        self.ctfSettings = Game_CTF()
        self.territoriesSettings = Game_Territories()
        self.zombiesSettings = Game_Zombies()
        self.teams = [Team() for _ in range(8)]
        self.teamScoring = Scoring(True)
        self.playerScoring = Scoring(False)
        self.stats = [Stats() for _ in range(8)]
        self.weapons = [Weapon() for _ in range(16)]
        self.powerups = [Powerup() for _ in range(16)]
        self.networkUnitProfiles = [NetworkUnitProfile() for _ in range(8)]
        """
        #self.networkUnitProfiles_sel = [0 for _ in range(8)]
        #self.networkUnitProfiles_ids = [[0 for _ in range(32)] for __ in range(8)]
        #self.networkUnitProfiles_pwrps = [[0 for _ in range(16)] for __ in range(8)]