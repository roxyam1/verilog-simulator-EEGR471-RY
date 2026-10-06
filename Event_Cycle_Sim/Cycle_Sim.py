import csv
import Sim_Setup
import sys
import os
import subprocess
from sys import argv
import Logic_Sim_Class
import Parser
import shutil

verilogPath = argv[1]
csvPath = argv[2]

def updateInputWires(rowInput, inputWires):
    updatedInputWires = inputWires
    for i, wire in enumerate(inputWires):
        if wire.getName() == columnNames[i+1]:
            updatedInputWires[i].newBoolValue(int(rowInput[i+1]))
    return updatedInputWires

def updateWireList(inputWires, wireList):
    updatedWires = wireList
    for i, wire in enumerate(inputWires):
            updatedWires[i]  = wire
    return updatedWires

[allWires, gates] = Sim_Setup.main(verilogPath)
inputWires = [wire for wire in allWires if wire.getLevel() == 0]

sortedGates = sorted(gates, key=lambda Gate: Gate.getLevel())

csvFile = []

with open(csvPath, newline='') as csvfile:
    vectorInputs = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in vectorInputs:
        csvFile.append(row)

columnNames = csvFile[0]
colSize =len(csvFile)
csvFile.pop(0)

shutil.copy(csvPath, "Event_Cycle_Sim/Result_Vectors/Cycle_Vectors")

rowSize = 0
for gate in sortedGates:
    if gate.getIsOutput():
        rowSize += 1


resultVectors = [[0] * rowSize for i in range(colSize)]
resultVectors[0] = []
for gate in sortedGates:
    if gate.getIsOutput():
        resultVectors[0].append(gate.getName())


rowIndex = 1
for row in csvFile:
    resultVectors[rowIndex] = []
    for gate in sortedGates:
        allWires = updateWireList(updateInputWires(row, inputWires),allWires)

        inputAName = (gate.getInputWireA()).getName()
        inputBName = (gate.getInputWireB()).getName()
        outputName = (gate.getOutputWire()).getName()

        for wire in allWires:
            if wire.getName() == inputAName:
                gate.updateInputWireA(wire)
            if wire.getName() == inputBName:
                gate.updateInputWireB(wire)

        gate.updateGate()

        for i, wire in enumerate(allWires):
            if wire.getName() == outputName:
                allWires[i] = gate.getOutputWire()

        if gate.getIsOutput():
            resultVectors[rowIndex].append(gate.getOutputWire().getBoolValue())
    rowIndex += 1

with open(csvPath,'r') as csvinput:
    with open("Event_Cycle_Sim/Result_Vectors/Cycle_Vectors/"+os.path.basename(csvPath), 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')

        for i, row in enumerate(csv.reader(csvinput)):
            row.extend(resultVectors[i])
            writer.writerow(row)

os.rename("Event_Cycle_Sim/Result_Vectors/Cycle_Vectors/"+os.path.basename(csvPath), "Event_Cycle_Sim/Result_Vectors/Cycle_Vectors/Cycle_Sim_Result_Vectors.csv")



