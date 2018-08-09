class ConfigData():
    brokerIP = None
    foxitPath = None
    scoresheetLines = ["Scoresheet Line 1", "Scoresheet Line 2", "Scoresheet Line 3", "Scoresheet Line 4"]
    ccards = [0 for _ in range(16)]
    names = ["Unnamed Device" for _ in range(96)]
    deviceTypes = [0 for _ in range(96)]
    serialNums = [0 for _ in range(96)]
    macs = [0 for _ in range(96)]
    twitterEnabled = False
    consumer_key = ""
    consumer_secret = ""
    token = ""
    token_secret = ""
    holsterCharging = False
    ignoreBatteryState = False
    phaserOnlyLowVoltage = "8.5"
    phaserLowVoltage = "9.5"
    phaserFirmware = ""
    networkUnitFirmware = ""
    rssiThreshold = "-89"

    def __init__(self):
        self.brokerIP = None
        self.foxitPath = None
        self.scoresheetLines = ["Scoresheet Line 1", "Scoresheet Line 2", "Scoresheet Line 3", "Scoresheet Line 4"]
        self.ccards = [0 for _ in range(16)]
        self.names = ["Unnamed Device" for _ in range(96)]
        self.deviceTypes = [0 for _ in range(96)]
        self.serialNums = [0 for _ in range(96)]
        self.macs = [0 for _ in range(96)]

        #Twitter
        self.twitterEnabled = False
        self.consumer_key = ""
        self.consumer_secret = ""
        self.token = ""
        self.token_secret = ""

        #Advanced
        self.holsterCharging = False
        self.ignoreBatteryState = False
        self.phaserOnlyLowVoltage = "8.5"
        self.phaserLowVoltage = "9.5"
        self.phaserFirmware = ""
        self.networkUnitFirmware = ""
        self.rssiThreshold = "-89"
