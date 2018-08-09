def GAME_PARTY_2_TEAM(gameSettings):
    gameSettings.IDname = "Party 2-Team"
    gameSettings.coreSettings.name = "Party Game"
    gameSettings.coreSettings.type = 0
    gameSettings.coreSettings.time = 20
    gameSettings.coreSettings.friendlyFireMode = 2

    gameSettings.classicSettings.gameMode = 0

    gameSettings.playerScoring.startingPoints = 20000

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
    gameSettings.weapons[0].fireRate = 2
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 0

    gameSettings.weapons[1].name = "Auto-Rifle"
    gameSettings.weapons[1].type = 1
    gameSettings.weapons[1].fireRate  = 3
    gameSettings.weapons[1].maxAmmo = -1
    gameSettings.weapons[1].mixedDamage = 0

    gameSettings.weapons[2].name = "Burst-Rifle"
    gameSettings.weapons[2].type = 4
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 0

    gameSettings.powerups[0].name = "Invulnerability"
    gameSettings.powerups[0].type = 3
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 15
    gameSettings.powerups[0].variableTwo = 1

    gameSettings.powerups[1].name = "Auto-Rifle"
    gameSettings.powerups[1].type = 6
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 60
    gameSettings.powerups[1].variableTwo = 1

    gameSettings.powerups[2].name = "Burst-Rifle Ammo"
    gameSettings.powerups[2].type = 5
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 50
    gameSettings.powerups[2].variableTwo = 2

    gameSettings.powerups[3].name = "Stealth Mode"
    gameSettings.powerups[3].type = 1
    gameSettings.powerups[3].maxCharges = 1
    gameSettings.powerups[3].variableOne = 30
    gameSettings.powerups[3].variableTwo = 0

    gameSettings.networkUnitProfiles[0].mode = 2
    gameSettings.networkUnitProfiles[0].powerups[0] = 1
    gameSettings.networkUnitProfiles[0].powerups[2] = 1
    gameSettings.networkUnitProfiles[0].powerups[3] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = -1
    gameSettings.networkUnitProfiles[0].ids[0] = True
    gameSettings.networkUnitProfiles[0].ids[1] = True
    gameSettings.networkUnitProfiles[0].ids[4] = True
    gameSettings.networkUnitProfiles[0].ids[5] = True

    gameSettings.networkUnitProfiles[1].mode = 1
    gameSettings.networkUnitProfiles[1].powerups[0] = 1
    gameSettings.networkUnitProfiles[1].powerups[2] = 1
    gameSettings.networkUnitProfiles[1].powerups[3] = 1
    gameSettings.networkUnitProfiles[1].deactivationTime = 30
    gameSettings.networkUnitProfiles[1].teamAffiliation = -1
    gameSettings.networkUnitProfiles[1].ids[2] = True
    gameSettings.networkUnitProfiles[1].ids[3] = True
    gameSettings.networkUnitProfiles[1].ids[6] = True
    gameSettings.networkUnitProfiles[1].ids[7] = True

    gameSettings.stats[0].maxHealth = -1
    gameSettings.stats[0].maxShield = 0
    gameSettings.stats[0].startingHealth = -1
    gameSettings.stats[0].startingShield = 0
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 0
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay =0
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_3 = -1
    gameSettings.stats[0].tagBonusPowerup_5 = 1
    gameSettings.stats[0].tagBonusPowerup_7 = -1
    gameSettings.stats[0].tagBonusPowerup_10 = -1
    gameSettings.stats[0].defShields = 30
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10

def GAME_PARTY_SOLO(gameSettings):
    gameSettings.IDname = "Party Solo"
    gameSettings.coreSettings.name = "Party - Solo"
    gameSettings.coreSettings.type = 0
    gameSettings.coreSettings.time = 20
    gameSettings.coreSettings.friendlyFireMode = 3


    gameSettings.classicSettings.gameMode = 0

    gameSettings.teams[0].setColour(255, 0, 0)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Solo"

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 2
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 0

    gameSettings.weapons[1].name = "Auto-Rifle"
    gameSettings.weapons[1].type = 1
    gameSettings.weapons[1].fireRate  = 3
    gameSettings.weapons[1].maxAmmo = -1
    gameSettings.weapons[1].mixedDamage = 0

    gameSettings.weapons[2].name = "Burst-Rifle"
    gameSettings.weapons[2].type = 4
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 0

    gameSettings.powerups[0].name = "Invulnerability"
    gameSettings.powerups[0].type = 3
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 15
    gameSettings.powerups[0].variableTwo = 1

    gameSettings.powerups[1].name = "Auto-Rifle"
    gameSettings.powerups[1].type = 6
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 60
    gameSettings.powerups[1].variableTwo = 1

    gameSettings.powerups[2].name = "Burst-Rifle Ammo"
    gameSettings.powerups[2].type = 5
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 50
    gameSettings.powerups[2].variableTwo = 2

    gameSettings.powerups[3].name = "Stealth Mode"
    gameSettings.powerups[3].type = 1
    gameSettings.powerups[3].maxCharges = 1
    gameSettings.powerups[3].variableOne = 30
    gameSettings.powerups[3].variableTwo = 0

    gameSettings.networkUnitProfiles[0].mode = 2
    gameSettings.networkUnitProfiles[0].powerups[0] = 1
    gameSettings.networkUnitProfiles[0].powerups[2] = 1
    gameSettings.networkUnitProfiles[0].powerups[3] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = -1
    gameSettings.networkUnitProfiles[0].ids[0] = True
    gameSettings.networkUnitProfiles[0].ids[1] = True
    gameSettings.networkUnitProfiles[0].ids[4] = True
    gameSettings.networkUnitProfiles[0].ids[5] = True

    gameSettings.networkUnitProfiles[1].mode = 1
    gameSettings.networkUnitProfiles[1].powerups[0] = 1
    gameSettings.networkUnitProfiles[1].powerups[2] = 1
    gameSettings.networkUnitProfiles[1].powerups[3] = 1
    gameSettings.networkUnitProfiles[1].deactivationTime = 30
    gameSettings.networkUnitProfiles[1].teamAffiliation = -1
    gameSettings.networkUnitProfiles[1].ids[2] = True
    gameSettings.networkUnitProfiles[1].ids[3] = True
    gameSettings.networkUnitProfiles[1].ids[6] = True
    gameSettings.networkUnitProfiles[1].ids[7] = True


    gameSettings.stats[0].maxHealth = -1
    gameSettings.stats[0].maxShield = 0
    gameSettings.stats[0].startingHealth = -1
    gameSettings.stats[0].startingShield = 0
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 0
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay =0
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_3 = -1
    gameSettings.stats[0].tagBonusPowerup_5 = 1
    gameSettings.stats[0].tagBonusPowerup_7 = -1
    gameSettings.stats[0].tagBonusPowerup_10 = -1
    gameSettings.stats[0].defShields = 30
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10