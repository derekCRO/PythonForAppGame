import time


class Device():
    def __init__(self, id):
        self.inUse = False
        self.netID = id
        self.lastCommunicationTime = 0
        self.lastActivityTime = 0
        self.type = None
        self.mac = int(0)
        self.serialNum = int(0)
        self.battery = 0
        self.batteryVoltage = float(0)
        self.charging = False
        self.name = "Unassigned Device"
        self.firmwareVersion = "Unknown"

    def isOnline(self):
        if(time.time() - self.lastCommunicationTime < 65):
            return True
        else:
            return False

    def isActive(self):
        if(time.time() - self.lastActivityTime < 60):
            return True
        else:
            return False

    def setName(self, newName):
        self.name = newName

    def assignDevice(self, type, mac, serialNum, name=""):
        if(type != 0):
            self.inUse = True
        else:
            self.inUse = False
        self.type = type
        self.mac = mac
        self.serialNum = serialNum
        if(name != ""):
            self.name = name

    def setDeviceFirmware(self, deviceFirmware):
        self.firmwareVersion = deviceFirmware

    def updateDeviceStatus(self, batteryVoltage, charging):
        self.batteryVoltage = batteryVoltage
        #self.battery = ?
        self.charging = charging
        self.lastCommunicationTime = time.time()

    def deassignDevice(self):
        self.inUse = False

    def kickCommunicationTimer(self):
        self.lastCommunicationTime = time.time()

    def kickActiveTimer(self):
        self.lastActivityTime = time.time()