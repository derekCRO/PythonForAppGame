def GAME_CTF_HEMEL(gameSettings):
    gameSettings.IDname = "CTF Hemel"
    gameSettings.coreSettings.name = "CTF Hemel"
    gameSettings.coreSettings.type = 0
    gameSettings.coreSettings.time = 15
    gameSettings.coreSettings.friendlyFireMode = 2
    gameSettings.classicSettings.gameMode = 0

    gameSettings.teams[0].setColour(60, 180, 255)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Blue Team"

    gameSettings.teams[1].setColour(255, 110, 35)
    gameSettings.teams[1].statsAssignment = 0
    gameSettings.teams[1].maximumPlayers = -1
    gameSettings.teams[1].name = "Orange Team"

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 1
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 1

    gameSettings.networkUnitProfiles[0].mode = 5
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = 0
    gameSettings.networkUnitProfiles[0].ids[4] = True

    gameSettings.networkUnitProfiles[1].mode = 5
    gameSettings.networkUnitProfiles[1].deactivationTime = 30
    gameSettings.networkUnitProfiles[1].teamAffiliation = 1
    gameSettings.networkUnitProfiles[1].ids[1] = True

    gameSettings.stats[0].maxHealth = 1
    gameSettings.stats[0].maxShield = 0
    gameSettings.stats[0].startingHealth = 1
    gameSettings.stats[0].startingShield = 0
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 0
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 0
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_3 = -1
    gameSettings.stats[0].tagBonusPowerup_5 = -1
    gameSettings.stats[0].tagBonusPowerup_7 = -1
    gameSettings.stats[0].tagBonusPowerup_10 = -1
    gameSettings.stats[0].defShields = 25
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10