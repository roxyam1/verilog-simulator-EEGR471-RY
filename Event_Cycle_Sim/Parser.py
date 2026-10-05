import Logic_Sim_Class
gateKeywords = ["AND","XOR","UNOT","OR"]

def main(parseInput):
    toBeParsed = parseInput;
    partiallyParsed = (((((((((((toBeParsed.replace("term","")).replace("Terminal ","")).replace(", 'Wire']","")).replace(" msb:(IntConst 0) lsb:(IntConst 0)","")).replace("Generating LALR tables WARNING: 183 shift/reduce conflicts Directive: Instance: ","")).replace("Operator ","")).replace("Bind:",""))).replace("[","")).replace("tree:","")).replace(" Next:","")).replace("'","")
    partiallyParsed = ((((partiallyParsed.replace("Term name:","name ")).replace("Bind dest:","ResultWire ")).replace(" Term: ","")).replace("msb","")).replace("lsb","")
    fullyParsedAst = (((partiallyParsed.replace(")","")).replace(",","")).replace("("," ")).split()
    for i in range(4):
        fullyParsedAst.pop(0);

    return fullyParsedAst;

if __name__ == "__main__":
    main()

def makeInputs(parsedAst):
    wireInputs = []
    classAst = parsedAst;
    for i in range(len(parsedAst)):
        if parsedAst[i] == "type:Input":
            tempVar = parsedAst[i-1]
            temp2 = (tempVar.split("."))
            wireInputs.append(Logic_Sim_Class.Wire(temp2[1],None,True))
            for j,k in enumerate(classAst):
                if tempVar == k:
                    classAst[j] = wireInputs[-1]
    return wireInputs, classAst;

def makeGates(parsedAst):
    cleanedAst = parsedAst
    simGates = []
    finalAst = []

    for point, entry in enumerate(cleanedAst):
       if type(entry) == str:
           if entry.upper() in gateKeywords:
                simGates.append(Logic_Sim_Class.Gate(None,None,None,entry.upper()));
                if cleanedAst[point-2] == "ResultWire":
                    simGates[-1].setOutput(True)
                    outputName = (cleanedAst[point-1]).split(".")
                    simGates[-1].changeName(outputName[1])
                else:
                    simGates[-1].setOutput(False)
                cleanedAst[point] = simGates[-1]
    for i in cleanedAst:
        if type(i) != str:
            finalAst.append(i)

    return finalAst, simGates;

def completeGates(parsedAst): # inputWires):
    moddedAst = parsedAst
    #outputWires = [] # inputWires
    completedGates = []
    gateKeywords = ["AND", "OR", "NOT", "UNOT"]
    i = 0
    while i < len(moddedAst):
        if type(moddedAst[i]) == Logic_Sim_Class.Gate:
            if moddedAst[i].getFunc() == "UNOT":
                completedGates.append(moddedAst[i])
                completedGates[-1].updateInputWireA(moddedAst[i+1])
                completedGates[-1].updateInputWireB(moddedAst[i+1])
                if not (moddedAst[i].getIsOutput()):
                    (completedGates[-1].changeName(moddedAst[i].getFunc()+"_"+moddedAst[i-1].getName()))

                completedGates[-1].setGateLevel()
                completedGates[-1].createOutputWire()
                (completedGates[-1].getOutputWire()).setWireLevel(completedGates[-1].getLevel())

                

                moddedAst[i] = completedGates[-1].getOutputWire()
                
                moddedAst.pop(i+1)
                moddedAst.append(completedGates[-1].getOutputWire())
            else:
                completedGates.append(moddedAst[i])
                completedGates[-1].updateInputWireA(moddedAst[i+1])
                completedGates[-1].updateInputWireB(moddedAst[i+2])

                if not (moddedAst[i].getIsOutput()):
                    (completedGates[-1].changeName(moddedAst[i].getFunc()+"_"+moddedAst[i-1].getName()+"_"+moddedAst[i-2].getName()))

                completedGates[-1].setGateLevel()
                completedGates[-1].createOutputWire()
                (completedGates[-1].getOutputWire()).setWireLevel(completedGates[-1].getLevel())
                moddedAst[i] = completedGates[-1].getOutputWire()
                
                moddedAst.pop(i+1)
                moddedAst.pop(i+1)
                moddedAst.append(completedGates[-1].getOutputWire())
            i = 0
        else:
            i += 1

    uniqueGates = []
    gateNames = []

    for i in completedGates:
        gateNames.append(i.getName())

    for i, gate in enumerate(completedGates):
        if gate.getName() not in gateNames[i+1:]:
            uniqueGates.append(gate)

    
    return uniqueGates # outputWires

def completeFanout(completedGates, inputs):
    tempWires = inputs
    finalWires = []
    for gate in completedGates:
        tempWires.append(gate.getOutputWire())
    wireNames = [wire.getName() for wire in tempWires]

    for wire in tempWires:
        temp = wire
        fanOut = []
        for gate in completedGates:
            wireA = (gate.getInputWireA()).getName()
            wireB = (gate.getInputWireB()).getName()
            if wire.getName() == wireA:
                temp.addFanout(gate.getName())
                fanOut.append(gate.getName())
            if wire.getName() == wireB:
                fanOut.append(gate.getName())

        uniqueWire = []
        for i, w in enumerate(fanOut):
            if w not in fanOut[i+1:]:
                uniqueWire.append(w)

        temp.newFanout(uniqueWire)

        finalWires.append(temp)
        fanOut = []
    
    return finalWires            
