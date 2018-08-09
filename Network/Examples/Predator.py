def GAME_PREDATOR(gameSettings):
    gameSettings.IDname = "Predator"
    gameSettings.coreSettings.name = "Predator"
    gameSettings.coreSettings.type = 0
    gameSettings.coreSettings.time = 10
    gameSettings.coreSettings.friendlyFireMode = 2
    gameSettings.classicSettings.gameMode = 0

    gameSettings.playerScoring.hitOpponent = 100
    gameSettings.playerScoring.hitByOpponent = 0
    gameSettings.playerScoring.hitOwnTeam = 0
    gameSettings.playerScoring.hitTarget = 0

    gameSettings.teamScoring.hitOpponent = 1
    gameSettings.teamScoring.hitByOpponent = 0
    gameSettings.teamScoring.hitOwnTeam = 0
    gameSettings.teamScoring.hitTarget = 0

    gameSettings.weapons[0].name = "Stun Blaster"
    gameSettings.weapons[0].type = 3
    gameSettings.weapons[0].fireRate = 1
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 1

    gameSettings.weapons[1].name = "Eliminator"
    gameSettings.weapons[1].type = 0
    gameSettings.weapons[1].fireRate = 1
    gameSettings.weapons[1].maxAmmo = -1
    gameSettings.weapons[1].mixedDamage = 1

    gameSettings.weapons[2].name = "M41A Rifle"
    gameSettings.weapons[2].type = 1
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 1

    gameSettings.powerups[0].name = "Stealth Mode"
    gameSettings.powerups[0].type = 1
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = -1
    gameSettings.powerups[0].variableTwo = 1

    gameSettings.powerups[1].name = "Shield Boost"
    gameSettings.powerups[1].type = 7
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 30
    gameSettings.powerups[1].variableTwo = 5

    gameSettings.powerups[2].name = "M41A Ammo"
    gameSettings.powerups[2].type = 5
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 50
    gameSettings.powerups[2].variableTwo = 2

    gameSettings.networkUnitProfiles[0].mode = 2
    gameSettings.networkUnitProfiles[0].powerups[1] = 1
    gameSettings.networkUnitProfiles[0].powerups[2] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = 0
    gameSettings.networkUnitProfiles[0].ids[8] = True

    gameSettings.stats[0].maxHealth = 10
    gameSettings.stats[0].maxShield = 0
    gameSettings.stats[0].startingHealth = 10
    gameSettings.stats[0].startingShield = 0
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 0
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 0
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].defShields = 25
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 5

    gameSettings.stats[1].maxHealth = 10
    gameSettings.stats[1].maxShield = 3
    gameSettings.stats[1].startingHealth = 10
    gameSettings.stats[1].startingShield = 3
    gameSettings.stats[1].healthRechargeRate = 0
    gameSettings.stats[1].shieldRechargeRate = 1
    gameSettings.stats[1].healthRechargeDelay = 0
    gameSettings.stats[1].shieldRechargeDelay = 100
    gameSettings.stats[1].weaponAmmo[1] = -1
    gameSettings.stats[1].powerupAmmo[0] = 1
    gameSettings.stats[1].defShields = 50
    gameSettings.stats[1].warnings = 0
    gameSettings.stats[1].reflex = 0

    gameSettings.teams[0].setColour(60, 180, 255)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Survivors"

    gameSettings.teams[1].setColour(0, 255, 0)
    gameSettings.teams[1].statsAssignment = 1
    gameSettings.teams[1].minimumPlayers = 3
    gameSettings.teams[1].maximumPlayers = 3
    gameSettings.teams[1].name = "Predators"
