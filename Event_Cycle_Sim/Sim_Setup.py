import sys
import os
import subprocess
from sys import argv
from unittest import result
import Logic_Sim_Class
import Parser
#FIRST ARGUMENT VALUE SHOULD BE THE PATH FOR THE VERILOG DESIGN
#SECOND ARGUMENT VALUE SHOULD BE THE PATH FOR THE CSV FILE

commandInputModName = "python3 pyverilog/examples/example_parser.py "  # Replace this with the command you want to run
commandInputAstTree = "python3 pyverilog/examples/example_dataflow_analyzer.py -t "

def main(vPath):
    verilogPath = vPath
    cmdOutput = None;

    result = subprocess.run(commandInputModName + '"' + verilogPath + '"', capture_output=True, text=True)
    output = (((result.stdout.strip()).replace("\n"," ")).split())
    moduleName = (output[output.index("ModuleDef:")+1])

    cmdOutput = ((subprocess.run(commandInputAstTree + moduleName + ' "' + verilogPath + '"', capture_output=True, text=True)).stdout.strip().replace("\n"," "))

    parsedList = (Parser.main(cmdOutput));

    [inputWires, parsedList] = Parser.makeInputs(parsedList);

    parsedList = parsedList[parsedList.index("ResultWire"):]

    [parsedList, gateList] = Parser.makeGates(parsedList);

    completedGates = Parser.completeGates(parsedList);

    finalWires = Parser.completeFanout(completedGates, inputWires);

    return finalWires, completedGates


if __name__ == "__main__":
    main()