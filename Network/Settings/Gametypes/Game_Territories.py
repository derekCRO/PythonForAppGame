
"""
TERRITORIES GAME MODE ENUMERATIONS:

- DOMINATION    0
- KINGOFTHEHILL 1
- TUGOFWAR      2
"""

class Game_Territories():
    def __init__(self):
        self.mode = 'DOMINATION'
        self.captureByTag = False       #capture by tag - true, capture by area - false
        self.neutralEnabled = True      #territory neutralisable
        self.hitsToCapture = 1          #ticks to neutralise or capture territory
        self.tickRate = 10              #time in 0.1 seconds per tick (eg, 5 = 0.5 seconds per tick = 2 ticks per second)
        self.numTerritories = 1         #number of territories

        self.kothTimeBeforeChange = 30  #time in seconds before hill change in koth

        self.towTimeBeforeChange = 30   #time after territory secured before next becomes contested