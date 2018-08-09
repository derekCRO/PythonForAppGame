"""
from Backend.Network.Settings.Class_Weapon import Weapon

from Backend.Network.Settings.Settings_Classes.Class_Powerup import Powerup


def ReadWeaponsFromFile(fileName):
    try:
        weaponsFile = open(fileName, "r")
    except:
        from tkinter import messagebox
        if(messagebox.askyesno(message="Failed to open weapons file. Create new one?") == True):
            weaponsFile = open(fileName, "w")
            wl("START WEAPONS FILE\n", weaponsFile)
            weaponsFile.close()
        else:
            return
    lines = weaponsFile.readlines()
    weaponsFile.close()
    weaponsList = []
    numOfWeapons = int((len(lines) - 3) / 11)
    for index in range(numOfWeapons):
        newWeapon = Weapon()
        newWeapon.IDname = lines[3+(index*11)].rstrip()
        newWeapon.name  = lines[4+(index*11)].rstrip()
        newWeapon.type = lines[5+(index*11)].rstrip()
        newWeapon.fireRate = lines[6+(index*11)].rstrip()
        newWeapon.maxAmmo = lines[7+(index*11)].rstrip()
        newWeapon.mixedDamage = lines[8+(index*11)].rstrip()
        newWeapon.healthDamage = lines[9+(index*11)].rstrip()
        newWeapon.shieldDamage = lines[10+(index*11)].rstrip()
        weaponsList.append(newWeapon)
    return weaponsList

def WriteWeaponsToFile(fileName, weaponsList):
    weaponsFile = open(fileName, "w")
    wl("START WEAPONS FILE\n", weaponsFile)
    for index, Weapon in enumerate(weaponsList):
        wl("START WEAPON " + str(index), weaponsFile)
        wl(Weapon.IDname, weaponsFile)
        wl(Weapon.name, weaponsFile)
        wl(Weapon.type, weaponsFile)
        wl(Weapon.fireRate, weaponsFile)
        wl(Weapon.maxAmmo, weaponsFile)
        wl(Weapon.mixedDamage, weaponsFile)
        wl(Weapon.healthDamage, weaponsFile)
        wl(Weapon.shieldDamage, weaponsFile)
        wl("END WEAPON\n",weaponsFile)
    wl("\nEND WEAPONS FILE", weaponsFile)
    weaponsFile.close()

def ReadPowerupsFromFile(fileName):
    try:
        powerupsFile = open(fileName, "r")
    except:
        from tkinter import messagebox
        if(messagebox.askyesno(message="Failed to open powerups file. Create new one?") == True):
            powerupsFile = open(fileName, "w")
            wl("START POWERUPS FILE\n", powerupsFile)
            powerupsFile.close()
            powerupsFile = open(fileName, "r")
        else:
            return
    lines = powerupsFile.readlines()
    powerupsFile.close()
    powerupsList = []
    numOfPowerups = int((len(lines) - 3) / 9)
    for index in range(numOfPowerups):
        newPowerup = Powerup()
        newPowerup.IDname = lines[3+(index*9)].rstrip()
        newPowerup.name  = lines[4+(index*9)].rstrip()
        newPowerup.type = lines[5+(index*9)].rstrip()
        newPowerup.maxCharges = lines[6+(index*9)].rstrip()
        newPowerup.variableOne = lines[7+(index*9)].rstrip()
        newPowerup.variableTwo = lines[8+(index*9)].rstrip()
        powerupsList.append(newPowerup)
    return powerupsList

def WritePowerupsToFile(fileName, powerupsList):
    powerupsFile = open(fileName, "w")
    wl("START POWERUPS FILE\n", powerupsFile)
    for index, Powerup in enumerate(powerupsList):
        wl("START POWERUP " + str(index), powerupsFile)
        wl(Powerup.IDname, powerupsFile)
        wl(Powerup.name, powerupsFile)
        wl(Powerup.type, powerupsFile)
        wl(Powerup.maxCharges, powerupsFile)
        wl(Powerup.variableOne, powerupsFile)
        wl(Powerup.variableTwo, powerupsFile)
        wl("END POWERUP\n",powerupsFile)
    wl("\nEND POWERUPS FILE", powerupsFile)
    powerupsFile.close()

def wl(string, file):
    file.write(str(string) + '\n')
"""