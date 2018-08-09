
"""
GAME MODE ENUMERATIONS:

- CLASSIC       0
- VIP           1
- JUGGERNAUT    2
- ELIMINATOR    3
- SCAVENGER     4

VIP ASSIGNMENT MODE:
- PER TEAM      0
- ONE           1

JUGGERNAUT TRANSFER MODE:

- SHOOTER       0
- RANDOM        1
- REVERSE       2
- NONE          3
"""

class Game_Classic():
    def __init__(self):
        self.gameMode = 0

        self.solo = False                   #only apply for classic, eliminator and scavenger game modes

        self.vipStatsNo = 0                 #stats to apply to VIP
        self.vipEliminationMode = False     #elimination mode
        self.vipAssignedPerTeam = 0     #assigned per team - true, one vip in total - false
        self.vipsPerTeam = 0                #VIPs per team

        self.juggernautStatsNo = 0          #stat sets to assign to juggernauts
        self.juggernautTransferMode = 0     #transfer mode
        self.juggernautMaxTransfers = 0     #maximum number of transfers

        self.eliminatorLives = 0            #number of times a player can be eliminated

        self.scavengerMoveDelay = 0         #time in seconds after tagged before moving
        self.scavengerPointsActive = 0      #number of points active
