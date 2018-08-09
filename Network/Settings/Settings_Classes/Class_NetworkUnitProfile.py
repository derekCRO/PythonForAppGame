"""
NETWORK UNIT MODE ENUMERATIONS :
- EFFECTS UNIT      0
- TARGET            1
- POWERUP TERMINAL  2
- FLAG STATION      3
- TERRITORY         4
- RECHARGER         5

NETWORK UNIT OUTPUT MODE:
- OFF               0
- ON                1
- FLASH             2

ONBOARD LEDS MODE:
- OFF               0
- FIXED             1
- FLASH             2

SOUND MODE:
- OFF               0
- NORMAL            1
- MUSIC             2
- MUSICONLY         3

"""

class NetworkUnitProfile():
    def __init__(self):
        self.IDname = "Unnamed"
        self.mode = 0
        self.outputMode = [ 0, 0, 0, 0 ]
        self.onboardLedsMode = 0
        self.soundMode = 0
        self.powerups = [ 0 ] * 16
        self.deactivationTime = 0
        self.flashTime = -1
        self.teamAffiliation = -1
        self.musicTrackNo = -1
        self.ids = [ False ] * 32

    def isDeviceInProfile(self, id):
        return self.ids[id-64]

    def addDeviceToProfile(self, id):
        self.ids[id-64] = True

    def removeDeviceFromProfile(self, id):
        self.ids[id-64] = False

    def clearProfile(self):
        for index in range(32):
            self.removePlayerFromTeam(index)


