powerup_types = ['Spy', 'Stealth', 'Stat Boost', 'Invulnerability', 'Deflector Shield', 'Ammo', 'Infinite Ammo', 'Shield Overload', 'Virus']

"""
POWERUP TYPES ENUMERATIONS :
- Spy               0
- Stealth           1
- Stat Boost        2
- Invulnerability   3
- Deflector Shield  4
- Ammo              5
- Infinite Ammo     6
- Shield Overload   7
- Virus             8
"""

class Powerup():
    def __init__(self):
        self.IDname = None
        self.name = None
        self.type = 0
        self.maxCharges = 0
        self.variableOne = 0
        self.variableTwo = 0