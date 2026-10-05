#For event based simulation to work a Wire must remember its previous logic value
#Wires have names as they can originate from a gate with a name
#The wireLevel is 0 if it is an input as all inputs have a level of 0

class Wire:
    #Previous value is set to None instead of 0 for the purpose of initialization
    #Wire level is none as it may be an input wire or a gate wire
    previousValue = None
    wireLevel = None

    #Fanout is an empty list to be filled with gate names
    fanOut = []

    #Wire gets a name, a setup value, and a level if it is an input wire
    def __init__(self, wireName, setupBoolValue, isInput):
        self.name = wireName
        self.booleanValue = setupBoolValue
        if isInput:
            self.wireLevel = 0 

    #Sets level of wire
    def setWireLevel(self, Level):
        self.wireLevel = Level

    #Returns wire of level
    def getLevel(self):
        return self.wireLevel

    #Updates the boolean value of the wire
    def newBoolValue(self,newValue):
        self.previousValue = self.booleanValue
        self.booleanValue = newValue

    #Takes the boolean value of the wire
    def getBoolValue(self):
        return self.booleanValue

    #Checks if the wire has changed and returns True if so
    def hasChanged(self):
        return self.previousValue != self.booleanValue  

    #Adds a gate to the fanout
    def addFanout(self, gateName):
        self.fanOut.append(gateName)

    def newFanout(self, newFanoutList):
        self.fanOut = newFanoutList

    #Returns the fanout
    def getFanout(self):
        return self.fanOut

    def getName(self):
        return self.name

#Each gate has an output wire so making a gate makes a wire
#To avoid creating a new class for NOR gates just enter the same input twice for the wires

class Gate:
    gateLevel = None
    outputLogic = None
    isOutput = None
    outputWire = None

    def __init__(self, gateName, wireInputA, wireInputB, gateFunction):
        self.name = gateName
        self.inputA = wireInputA
        self.inputB = wireInputB
        self.gateType = gateFunction.upper()

    def getGateLevel(self):
        return self.gateLevel

    def setOutput(self, isOutput):
        self.isOutput = isOutput

    def setWires(self, wireInA, wireInB):
        self.inputA = wireInA
        self.inputB = wireInB
        self.inputA.addFanout(self.name)
        #if self.gateType!="UNOT":
         #   self.inputB.addFanout(self.name)

    def changeName(self, newName):
        self.name = newName

    def createOutputWire(self):
        self.outputWire = Wire(self.name,self.outputLogic,False)
    
    def getName(self):
        return self.name
    
    def getFunc(self):
        return self.gateType
    
    def getOutputValue(self):
        return self.outputLogic

    def updateWire(self):
        self.outputWire.newBoolValue(self.outputLogic)

    def setGateLevel(self):
        self.gateLevel = max(self.inputA.getLevel(), self.inputB.getLevel()) + 1

    def getOutputWire(self):
        return self.outputWire

    def getInputWireA(self):
        return self.inputA

    def getInputWireB(self):
        return self.inputB

    def getIsOutput(self):
        return self.isOutput
    
    def evaluateLogic(self):
        if self.gateType == "AND":
            return (self.inputA.getBoolValue() * self.inputB.getBoolValue())
        elif self.gateType == "OR":
            return (((self.inputA.getBoolValue() + self.inputB.getBoolValue())>=1)*1)
        elif self.gateType == "XOR":
            return ((self.inputA.getBoolValue()!=self.inputB.getBoolValue())*1)
        elif self.gateType == "UNOT":
            return (not (self.inputA.getBoolValue()*True))*1
    
    def changeFunction(self,newFunc):
        self.gateFunction = newFunc.upper()
    
    def updateGate(self):
        self.outputLogic = self.evaluateLogic()
        self.updateWire()

    def updateInputWireA(self, inWireA):
        self.inputA = inWireA

    def updateInputWireB(self, inWireB):
        self.inputB = inWireB
#Wire get fanout might not function correctly but it needs to be in an actual test to figure out the issue