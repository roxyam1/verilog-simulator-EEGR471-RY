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
csvFile.pop(0)

updateQueue = []

updatedWires = [["time","signal","value"]]



for row in csvFile:
    for gate in sortedGates:
        allWires = updateWireList(updateInputWires(row, inputWires),allWires)

        for wire in allWires:
            if wire.getLevel() == 0:
                if wire.hasChanged():
                    updatedWires.append([row[0], wire.getName(), wire.getBoolValue()])

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
            if (gate.getOutputWire()).hasChanged():
                updatedWires.append([row[0],gate.getOutputWire().getName(), gate.getOutputWire().getBoolValue()])

shutil.copy(csvPath, "Event_Cycle_Sim/Result_Vectors/Cycle_Vectors")

os.rename("Event_Cycle_Sim/Result_Vectors/Cycle_Vectors/"+os.path.basename(csvPath), "Event_Cycle_Sim/Result_Vectors/Event_Vectors/Event_Sim_Result_Vectors.csv")

with open("Event_Cycle_Sim/Result_Vectors/Event_Vectors/Event_Sim_Result_Vectors.csv", 'w') as csvOut:
    writer = csv.writer(csvOut, lineterminator='\n')
    for row in updatedWires:
        writer.writerow(row)