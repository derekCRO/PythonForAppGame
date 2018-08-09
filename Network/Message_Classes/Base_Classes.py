class MessageBaseClass():
    def __init__(self, topic="", message="", type=""):
        self.topicString = topic
        self.messageString = message
        self.type = type

class IncomingMessage(MessageBaseClass):
    def getPayload(self):
        return self.messageString[18:].split(':')
    def getMAC(self):
        return int(self.messageString.split('-')[0].replace(':', ''), 16)

class OutgoingMessage(MessageBaseClass):
    def assemblePayload(self, parameters):
        string = ""
        for i in range(len(parameters)-1):
            string += str(parameters[i])
            string += ':'
        string += str(parameters[len(parameters)-1])
        return string

    def assembleTopicWithSet(self, topicString, setNo):
        string = topicString
        if(setNo < 10):
            string += "0"
        string += str(setNo)
        return string

    def assembleTopicWithNetID(self, topicString, netID):
        string = topicString
        if(netID < 100):
            string += "0"
        if(netID < 10):
            string += "0"
        string += (str(netID))
        return string


    """
    DEPRECATED
    def assembleTopic(self, netID, postTopic):
        string = "QNET/"
        if(netID < 100):
            string += "0"
        if(netID < 10):
            string += "0"
        string += (str(netID) + "/")
        string += postTopic
        return string

    def assembleTopicWithSetNo(self, netID, postTopic, setNo):
        string = "QNET/"
        if(netID < 100):
            string += "0"
        if(netID < 10):
            string += "0"
        string += (str(netID) + "/")
        string += postTopic
        string += "/"
        if(setNo < 10):
            string += "0"
        string += (str(setNo))
        return string
    """