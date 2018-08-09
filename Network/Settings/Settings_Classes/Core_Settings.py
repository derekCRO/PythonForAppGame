
"""
GAME TYPE ENUMERATIONS:
- CLASSIC           0
- TERRITORIES       1
- CAPTURE-THE-FLAG  2
- ZOMBIES           3

FRIENDLY FIRE ENUMERATIONS:
- LETHAL            0
- NON-LETHAL        1
- OFF               2
- SOLO              3
"""

class Core_Settings():
    def __init__(self):
        self.name = "Unnamed Game"
        self.type = 0
        self.time = 20
        self.friendlyFireMode = 2
        self.twoHandsEnabled = True
        self.epilepsyMode = False