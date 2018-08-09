
class Stats():
    def __init__(self):
        self.IDname = None
        self.maxHealth = 100
        self.maxShield = 100
        self.startingHealth = 100
        self.startingShield = 100
        self.healthRechargeRate = 0
        self.shieldRechargeRate = 1
        self.healthRechargeDelay = 0
        self.shieldRechargeDelay = 10
        self.weaponAmmo = [0] * 16
        self.powerupAmmo = [0] * 16
        self.tagBonusPowerup_3 = -1
        self.tagBonusPowerup_5 = -1
        self.tagBonusPowerup_7 = -1
        self.tagBonusPowerup_10 = -1
        self.defShields         = 40
        self.warnings           = 0
        self.reflex             = 10
