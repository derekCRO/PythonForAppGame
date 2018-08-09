def GAME_ADVANCED_2_TEAM(gameSettings):
    #core settings
    gameSettings.IDname = "Advanced 2 Team"
    gameSettings.coreSettings.name = "Advanced"
    gameSettings.coreSettings.type = 0              #classic
    gameSettings.coreSettings.time = 20              #ten minutes
    gameSettings.coreSettings.friendlyFireMode = 2  #off

    gameSettings.classicSettings.gameMode = 0       #classic

    gameSettings.teams[0].setColour(255, 0, 0)              #red
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Red Team"

    gameSettings.teams[1].setColour(0, 255, 0)                #green
    gameSettings.teams[1].statsAssignment = 0
    gameSettings.teams[1].maximumPlayers = -1
    gameSettings.teams[1].name = "Green Team"

    gameSettings.powerups[0].name = "Spy Mode"
    gameSettings.powerups[0].type = 0
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 30
    gameSettings.powerups[0].variableTwo = 0

    gameSettings.powerups[1].name = "Stealth Mode"
    gameSettings.powerups[1].type = 1
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 30
    gameSettings.powerups[1].variableTwo = 0

    gameSettings.powerups[2].name = "Invulnerable Mode"
    gameSettings.powerups[2].type = 3
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 15
    gameSettings.powerups[2].variableTwo = 1

    gameSettings.powerups[3].name = "Auto Rifle Ammo"
    gameSettings.powerups[3].type = 5
    gameSettings.powerups[3].maxCharges = 1
    gameSettings.powerups[3].variableOne = 25
    gameSettings.powerups[3].variableTwo = 1

    gameSettings.powerups[4].name = "Shield Overload"
    gameSettings.powerups[4].type = 7
    gameSettings.powerups[4].maxCharges = 1
    gameSettings.powerups[4].variableOne = 30
    gameSettings.powerups[4].variableTwo = 100

    gameSettings.powerups[5].name = "Burst Rifle Ammo"
    gameSettings.powerups[5].type = 5
    gameSettings.powerups[5].maxCharges = 1
    gameSettings.powerups[5].variableOne = 30
    gameSettings.powerups[5].variableTwo = 2

    gameSettings.powerups[6].name = "Sniper Ammo"
    gameSettings.powerups[6].type = 5
    gameSettings.powerups[6].maxCharges = 1
    gameSettings.powerups[6].variableOne = 5
    gameSettings.powerups[6].variableTwo = 3

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 2
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 10

    gameSettings.weapons[1].name = "Auto Rifle"
    gameSettings.weapons[1].type = 1
    gameSettings.weapons[1].fireRate = 5
    gameSettings.weapons[1].maxAmmo = 50
    gameSettings.weapons[1].healthDamage = 10
    gameSettings.weapons[1].shieldDamage = 5

    gameSettings.weapons[2].name = "Burst-Rifle"
    gameSettings.weapons[2].type = 4
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 10

    gameSettings.weapons[3].name = "Sniper"
    gameSettings.weapons[3].type = 2
    gameSettings.weapons[3].fireRate = 1
    gameSettings.weapons[3].maxAmmo = 5
    gameSettings.weapons[3].mixedDamage = 25

    gameSettings.stats[0].maxHealth = 150
    gameSettings.stats[0].maxShield = 25
    gameSettings.stats[0].startingHealth = 150
    gameSettings.stats[0].startingShield = 25
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 1
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 75
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_5 = 3
    gameSettings.stats[0].tagBonusPowerup_10 = 2
    gameSettings.stats[0].defShields = 40
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10

    gameSettings.networkUnitProfiles[0].mode = 1                #team 0 targets
    gameSettings.networkUnitProfiles[0].powerups[0] = 1
    gameSettings.networkUnitProfiles[0].powerups[1] = 1
    gameSettings.networkUnitProfiles[0].powerups[4] = 1
    gameSettings.networkUnitProfiles[0].powerups[5] = 1
    gameSettings.networkUnitProfiles[0].powerups[6] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = 1
    gameSettings.networkUnitProfiles[0].ids[3] = True
    gameSettings.networkUnitProfiles[0].ids[7] = True

    gameSettings.networkUnitProfiles[1].mode = 1                #team 1 targets
    gameSettings.networkUnitProfiles[1].powerups[0] = 1
    gameSettings.networkUnitProfiles[1].powerups[1] = 1
    gameSettings.networkUnitProfiles[1].powerups[4] = 1
    gameSettings.networkUnitProfiles[1].powerups[5] = 1
    gameSettings.networkUnitProfiles[1].powerups[6] = 1
    gameSettings.networkUnitProfiles[1].deactivationTime = 30
    gameSettings.networkUnitProfiles[1].teamAffiliation = 0
    gameSettings.networkUnitProfiles[1].ids[2] = True
    gameSettings.networkUnitProfiles[1].ids[6] = True

    gameSettings.networkUnitProfiles[2].mode = 5
    gameSettings.networkUnitProfiles[2].deactivationTime = 0
    gameSettings.networkUnitProfiles[2].teamAffiliation = 1
    gameSettings.networkUnitProfiles[2].ids[0] = True
    gameSettings.networkUnitProfiles[2].ids[4] = True

    gameSettings.networkUnitProfiles[3].mode = 5
    gameSettings.networkUnitProfiles[3].deactivationTime = 30
    gameSettings.networkUnitProfiles[3].teamAffiliation = 0
    gameSettings.networkUnitProfiles[3].ids[1] = True
    gameSettings.networkUnitProfiles[3].ids[5] = True

def GAME_ADVANCED_3_TEAM(gameSettings):
    #core settings
    gameSettings.IDname = "Advanced 3 Team"
    gameSettings.coreSettings.name = "Advanced"
    gameSettings.coreSettings.type = 0              #classic
    gameSettings.coreSettings.time = 20              #ten minutes
    gameSettings.coreSettings.friendlyFireMode = 2  #off

    gameSettings.classicSettings.gameMode = 0       #classic

    gameSettings.teams[0].setColour(255, 0, 0)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Red Team"

    gameSettings.teams[1].setColour(0, 255, 0)
    gameSettings.teams[1].statsAssignment = 0
    gameSettings.teams[1].maximumPlayers = -1
    gameSettings.teams[1].name = "Green Team"

    gameSettings.teams[2].setColour(0, 0, 255)
    gameSettings.teams[2].statsAssignment = 0
    gameSettings.teams[2].maximumPlayers = -1
    gameSettings.teams[2].name = "Blue Team"

    gameSettings.powerups[0].name = "Spy Mode"
    gameSettings.powerups[0].type = 0
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 30
    gameSettings.powerups[0].variableTwo = 0

    gameSettings.powerups[1].name = "Stealth Mode"
    gameSettings.powerups[1].type = 1
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 30
    gameSettings.powerups[1].variableTwo = 0

    gameSettings.powerups[2].name = "Invulnerable Mode"
    gameSettings.powerups[2].type = 3
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 15
    gameSettings.powerups[2].variableTwo = 1

    gameSettings.powerups[3].name = "Auto Rifle Ammo"
    gameSettings.powerups[3].type = 5
    gameSettings.powerups[3].maxCharges = 1
    gameSettings.powerups[3].variableOne = 25
    gameSettings.powerups[3].variableTwo = 1

    gameSettings.powerups[4].name = "Shield Overload"
    gameSettings.powerups[4].type = 7
    gameSettings.powerups[4].maxCharges = 1
    gameSettings.powerups[4].variableOne = 30
    gameSettings.powerups[4].variableTwo = 100

    gameSettings.powerups[5].name = "Burst Rifle Ammo"
    gameSettings.powerups[5].type = 5
    gameSettings.powerups[5].maxCharges = 1
    gameSettings.powerups[5].variableOne = 30
    gameSettings.powerups[5].variableTwo = 2

    gameSettings.powerups[6].name = "Sniper Ammo"
    gameSettings.powerups[6].type = 5
    gameSettings.powerups[6].maxCharges = 1
    gameSettings.powerups[6].variableOne = 5
    gameSettings.powerups[6].variableTwo = 3

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 2
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 10

    gameSettings.weapons[1].name = "Auto Rifle"
    gameSettings.weapons[1].type = 1
    gameSettings.weapons[1].fireRate = 5
    gameSettings.weapons[1].maxAmmo = 50
    gameSettings.weapons[1].healthDamage = 10
    gameSettings.weapons[1].shieldDamage = 5

    gameSettings.weapons[2].name = "Burst-Rifle"
    gameSettings.weapons[2].type = 4
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 10

    gameSettings.weapons[3].name = "Sniper"
    gameSettings.weapons[3].type = 2
    gameSettings.weapons[3].fireRate = 1
    gameSettings.weapons[3].maxAmmo = 5
    gameSettings.weapons[3].mixedDamage = 25

    gameSettings.stats[0].maxHealth = 150
    gameSettings.stats[0].maxShield = 25
    gameSettings.stats[0].startingHealth = 150
    gameSettings.stats[0].startingShield = 25
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 1
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 75
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_5 = 3
    gameSettings.stats[0].tagBonusPowerup_10 = 2
    gameSettings.stats[0].defShields = 40
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10

    gameSettings.networkUnitProfiles[0].mode = 1
    gameSettings.networkUnitProfiles[0].powerups[0] = 1
    gameSettings.networkUnitProfiles[0].powerups[1] = 1
    gameSettings.networkUnitProfiles[0].powerups[4] = 1
    gameSettings.networkUnitProfiles[0].powerups[5] = 1
    gameSettings.networkUnitProfiles[0].powerups[6] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = -1
    gameSettings.networkUnitProfiles[0].ids[3] = True
    gameSettings.networkUnitProfiles[0].ids[7] = True
    gameSettings.networkUnitProfiles[0].ids[2] = True
    gameSettings.networkUnitProfiles[0].ids[6] = True

    gameSettings.networkUnitProfiles[1].mode = 5
    gameSettings.networkUnitProfiles[1].deactivationTime = 0
    gameSettings.networkUnitProfiles[1].teamAffiliation = -1
    gameSettings.networkUnitProfiles[1].ids[0] = True
    gameSettings.networkUnitProfiles[1].ids[4] = True
    gameSettings.networkUnitProfiles[1].ids[1] = True
    gameSettings.networkUnitProfiles[1].ids[5] = True

def GAME_ADVANCED_SOLO(gameSettings):
    #core settings
    gameSettings.IDname = "Advanced Solo"
    gameSettings.coreSettings.name = "Advanced - Solo"
    gameSettings.coreSettings.type = 0
    gameSettings.coreSettings.time = 20
    gameSettings.coreSettings.friendlyFireMode = 3

    gameSettings.classicSettings.gameMode = 0

    gameSettings.teams[0].setColour(255, 0, 0)
    gameSettings.teams[0].statsAssignment = 0
    gameSettings.teams[0].maximumPlayers = -1
    gameSettings.teams[0].name = "Solo"

    gameSettings.powerups[0].name = "Spy Mode"
    gameSettings.powerups[0].type = 0
    gameSettings.powerups[0].maxCharges = 1
    gameSettings.powerups[0].variableOne = 30
    gameSettings.powerups[0].variableTwo = 0

    gameSettings.powerups[1].name = "Stealth Mode"
    gameSettings.powerups[1].type = 1
    gameSettings.powerups[1].maxCharges = 1
    gameSettings.powerups[1].variableOne = 30
    gameSettings.powerups[1].variableTwo = 0

    gameSettings.powerups[2].name = "Invulnerable Mode"
    gameSettings.powerups[2].type = 3
    gameSettings.powerups[2].maxCharges = 1
    gameSettings.powerups[2].variableOne = 15
    gameSettings.powerups[2].variableTwo = 1

    gameSettings.powerups[3].name = "Auto Rifle Ammo"
    gameSettings.powerups[3].type = 5
    gameSettings.powerups[3].maxCharges = 1
    gameSettings.powerups[3].variableOne = 25
    gameSettings.powerups[3].variableTwo = 1

    gameSettings.powerups[4].name = "Shield Overload"
    gameSettings.powerups[4].type = 7
    gameSettings.powerups[4].maxCharges = 1
    gameSettings.powerups[4].variableOne = 30
    gameSettings.powerups[4].variableTwo = 100

    gameSettings.powerups[5].name = "Burst Rifle Ammo"
    gameSettings.powerups[5].type = 5
    gameSettings.powerups[5].maxCharges = 1
    gameSettings.powerups[5].variableOne = 30
    gameSettings.powerups[5].variableTwo = 2

    gameSettings.powerups[6].name = "Sniper Ammo"
    gameSettings.powerups[6].type = 5
    gameSettings.powerups[6].maxCharges = 1
    gameSettings.powerups[6].variableOne = 5
    gameSettings.powerups[6].variableTwo = 3

    gameSettings.weapons[0].name = "Phaser"
    gameSettings.weapons[0].type = 0
    gameSettings.weapons[0].fireRate = 2
    gameSettings.weapons[0].maxAmmo = -1
    gameSettings.weapons[0].mixedDamage = 10

    gameSettings.weapons[1].name = "Auto Rifle"
    gameSettings.weapons[1].type = 1
    gameSettings.weapons[1].fireRate = 5
    gameSettings.weapons[1].maxAmmo = 50
    gameSettings.weapons[1].healthDamage = 10
    gameSettings.weapons[1].shieldDamage = 5

    gameSettings.weapons[2].name = "Burst-Rifle"
    gameSettings.weapons[2].type = 4
    gameSettings.weapons[2].fireRate = 3
    gameSettings.weapons[2].maxAmmo = 50
    gameSettings.weapons[2].mixedDamage = 10

    gameSettings.weapons[3].name = "Sniper"
    gameSettings.weapons[3].type = 2
    gameSettings.weapons[3].fireRate = 1
    gameSettings.weapons[3].maxAmmo = 5
    gameSettings.weapons[3].mixedDamage = 25

    gameSettings.stats[0].maxHealth = 150
    gameSettings.stats[0].maxShield = 25
    gameSettings.stats[0].startingHealth = 150
    gameSettings.stats[0].startingShield = 25
    gameSettings.stats[0].healthRechargeRate = 0
    gameSettings.stats[0].shieldRechargeRate = 1
    gameSettings.stats[0].healthRechargeDelay = 0
    gameSettings.stats[0].shieldRechargeDelay = 75
    gameSettings.stats[0].weaponAmmo[0] = -1
    gameSettings.stats[0].tagBonusPowerup_5 = 3
    gameSettings.stats[0].tagBonusPowerup_10 = 2
    gameSettings.stats[0].defShields = 40
    gameSettings.stats[0].warnings = 0
    gameSettings.stats[0].reflex = 10

    gameSettings.networkUnitProfiles[0].mode = 1
    gameSettings.networkUnitProfiles[0].powerups[1] = 1
    gameSettings.networkUnitProfiles[0].powerups[4] = 1
    gameSettings.networkUnitProfiles[0].powerups[5] = 1
    gameSettings.networkUnitProfiles[0].powerups[6] = 1
    gameSettings.networkUnitProfiles[0].deactivationTime = 30
    gameSettings.networkUnitProfiles[0].teamAffiliation = -1
    gameSettings.networkUnitProfiles[0].ids[3] = True
    gameSettings.networkUnitProfiles[0].ids[7] = True
    gameSettings.networkUnitProfiles[0].ids[2] = True
    gameSettings.networkUnitProfiles[0].ids[6] = True

    gameSettings.networkUnitProfiles[1].mode = 5
    gameSettings.networkUnitProfiles[2].deactivationTime = 0
    gameSettings.networkUnitProfiles[2].teamAffiliation = -1
    gameSettings.networkUnitProfiles[1].ids[0] = True
    gameSettings.networkUnitProfiles[1].ids[4] = True
    gameSettings.networkUnitProfiles[1].ids[1] = True
    gameSettings.networkUnitProfiles[1].ids[5] = True