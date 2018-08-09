class Scoring():
    def __init__(self, team):
        self.active = False
        self.name = "Unnamed"
        self.description = "No Description"
        self.team = team

        if(team):
            self.startingPoints = 0
            self.hitOpponent = 2
            self.hitByOpponent = -1
            self.hitOwnTeam = -1
            self.hitTarget = 10

            self.hitVIP = 10
            self.hitByVIP = -1

            self.hitJuggernaut = 10
            self.hitByJuggernaut = -1

            self.capturedTerritory = 0
            self.heldTerritory = 5

            self.tookFlag = 0
            self.capturedFlag = 25
            self.hitFlagCarrier = 0

            self.survivorTaggedZombie = 3
            self.survivorTaggedByZombie = -1
            self.zombieTaggedSurvivor = 0
            self.zombieTaggedBySurvivor = 0
            self.survivorTaggedSurvivor = 3
            self.survivorTaggedBySurvivor = 0
            self.survivorTurnedToZombie = -5
            self.alphaTaggedBySurvivor = -1
            self.alphaTaggedSurvivor = 3
            self.zombieTurnedSurvivor = 0
        else:
            self.startingPoints = 0
            self.hitOpponent = 200
            self.hitByOpponent = -100
            self.hitOwnTeam = -100
            self.hitTarget = 1000

            self.hitVIP = 1000
            self.hitByVIP = -100

            self.hitJuggernaut = 1000
            self.hitByJuggernaut = -100

            self.capturedTerritory = 1000
            self.heldTerritory = 500

            self.tookFlag = 250
            self.capturedFlag = 2500
            self.hitFlagCarrier = 250

            self.survivorTaggedZombie = 300
            self.survivorTaggedByZombie = -100
            self.zombieTaggedSurvivor = 100
            self.zombieTaggedBySurvivor = -25
            self.survivorTaggedSurvivor = 300
            self.survivorTaggedBySurvivor = 300
            self.survivorTurnedToZombie = -5000
            self.alphaTaggedBySurvivor = -100
            self.alphaTaggedSurvivor = 300
            self.zombieTurnedSurvivor = 5000
