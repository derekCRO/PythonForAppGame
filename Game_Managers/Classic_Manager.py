
#pure storage classes for the backend manager

class Classic_Manager():
    def __init__(self):
        self.reset()

    def reset(self):
        self.vip_IDs = [-1]

        self.juggernaut_ID = [-1]
        self.juggernaut_transferCount = 0

        self.scavenger_activeID = [-1]