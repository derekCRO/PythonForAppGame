
weapon_types = ['Standard', 'Auto-Rifle', 'Sniper', 'Blaster', 'Burst-Rifle', 'System Hack', 'Recharger', 'Nanovirus', 'Restore', 'Sabotage']

"""
WEAPON TYPES ENUMERATIONS :
- Standard          0
- Auto-Rifle        1
- Sniper            2
- Blaster           3
- Burst-Rifle       4
- System Hack       5
- Recharger         6
- Nanovirus         7
- Restore           8
- Sabotage          9
- Flag              10
"""

class Weapon():
    def __init__(self):

        self.IDname = None
        self.name = None
        self.type = 0
        self.fireRate = 0
        self.maxAmmo = 0
        self.mixedDamage = 0
        self.healthDamage = 0
        self.shieldDamage = 0

