
class Team():
    def __init__(self):
        self.id = None
        self.red = 0
        self.green = 0
        self.blue = 0
        self.name = "Unnamed Team"
        self.playerIDs = [False] * 64
        self.statsAssignment = 0
        self.minimumPlayers = 0
        self.maximumPlayers = 0

    def isPlayerInTeam(self, id):
        return self.playerIDs[id]

    def addPlayerToTeam(self, id):
        self.playerIDs[id] = True

    def removePlayerFromTeam(self, id):
        self.playerIDs[id] = False

    def clearTeam(self, id):
        for index in range(64):
            self.removePlayerFromTeam(index)

    def setColour(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def getStats(self):
        return self.statsAssignment

    def getIDListForMessage(self):
        return self.playerIDs