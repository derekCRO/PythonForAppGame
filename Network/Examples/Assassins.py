def GAME_ASSASSINS(gameSettings):
    #core settings
    gameSettings.IDname = "Assassins"
    gameSettings.coreSettings.name = "Assassins"
    gameSettings.coreSettings.type = 0              #classic
    gameSettings.coreSettings.time = 5              #ten minutes
    gameSettings.coreSettings.friendlyFireMode = 3  #off

    gameSettings.classicSettings.gameMode = 0       #classic

    gameSettings.teams[0].setColour(0, 0, 0)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Solo"

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 1
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 3

    gameSettings.weapons[1].name = "Burst Rifle"
    gameSettings.weapons[1].type = 4
    gameSettings.weapons[1].fireRate = 3
    gameSettings.weapons[1].maxAmmo = 15
    gameSettings.weapons[1].mixedDamage = 5

    gameSettings.weapons[2].name = "Sniper Rifle"
    gameSettings.weapons[2].type = 2
    gameSettings.weapons[2].fireRate = 1
    gameSettings.weapons[2].maxAmmo = 3
    gameSettings.weapons[2].mixedDamage = 10

    gameSettings.powerups[0].name = "Burst Rifle Ammo"
    gameSettings.powerups[0].type = 5
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 15
    gameSettings.powerups[0].variableTwo = 1

    gameSettings.powerups[1].name = "Sniper Rifle Ammo"
    gameSettings.powerups[1].type = 5
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 3
    gameSettings.powerups[1].variableTwo = 2

    gameSettings.stats[0].maxHealth = 30
    gameSettings.stats[0].maxShield = 0
    gameSettings.stats[0].startingHealth = 30
    gameSettings.stats[0].startingShield = 0
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 0
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 0
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].defShields = 50
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 0

    gameSettings.networkUnitProfiles[0].mode = 2
    gameSettings.networkUnitProfiles[0].powerups[0] = 1
    gameSettings.networkUnitProfiles[0].powerups[1] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 15
    gameSettings.networkUnitProfiles[0].teamAffiliation = -1
    gameSettings.networkUnitProfiles[0].ids[8] = True


    #NU01 - 2460340 - Fut Base              65
    #NU02 - 2460420 - War Base              67
    #NU03 - 2471150 - Medi Base
    #NU04 - 2471960 - Wild Base


    return gameSettings