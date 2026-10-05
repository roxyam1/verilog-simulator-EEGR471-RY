# verilog-simulator-EEGR471-RY
Designed by Safee Al-Deen and Roxan Yamonche

# Architecture
Program includes a file of classes used to define each gate and wire in the circuit. The setup file takes the file path of the verilog file and runs the parser file which contains functions that fully initialize the gates and wires. Once the setup has been run the event based simulator adds each output wire that changes to the output CSV file, the cycle based simulator appends the output to the CSV file that includes the inputs.


# Requirements:
Python 3.14 or greater ()

Pyverilog (https://github.com/PyHDI/Pyverilog)

# Instructions
The simulator takes absolute paths for the verilog and python file. The output is saved in a CSV file under the Result_Vectors folder. The results should be removed from the folder after each simulation to avoid errors.


__python Event_Cycle_Sim/Event_Sim.py python "ABSOLUTE PATH FOR VERILOG FILE" "ABSOLUTE PATH FOR VECTOR INPUT"__  


The output is saved under Event_Cycle_Sim/Result_Vectors/Event_Vectors

# Analysis Questions

1. What is the primary difference between cycle-based and event-based simulation?
Every input-vector time step is evaluated by a cycle-based simulator, which typically assesses all modeled assignments. Only logic that is dependent on signal changes is evaluated by an event-based simulator.

2. If a 10,000-signal design has only two changing signals, which approach performs more unnecessary evaluation? Explain.
The cycle-based approach may reevaluate the entire modeled circuit at each simulation step, which results in more needless examination. Unrelated logic is left unevaluated since the event-based approach starts with the two modified signals and only follows their dependency chains.

3. Why can event-based simulation be advantageous for large digital systems?
Numerous signals that stay constant for extended periods of time can be found in large systems. When switching activity is scarce, event-based simulation can minimize computation by avoiding the need to continually evaluate stable, unrelated logic.

4. What additional data structures or algorithms does event-based simulation require?
An event queue, signal-state storage, dependency or fan-out data, and event scheduling and processing methods are all necessary. When processing events in simulation-time order, a priority queue can be helpful.

5. How does the dependency graph improve simulation efficiency?
The graph shows which assignments may be impacted by a signal change. As a result, rather of scanning and assessing each assignment, the simulator can simply assess pertinent tasks.

6. What must be added to support delays, clock edges, blocking/nonblocking assignments, and concurrent processes?
Richer time models, future-event scheduling, edge detection, procedural-process representation, blocking and nonblocking assignment semantics, process scheduling rules, and more comprehensive AST support would all be necessary for the simulator. Instead of instantly altering the signal, nonblocking assignments would necessitate scheduling updates in accordance with the proper simulation phase.

# Limitations
The simulator supports only the restricted combinational continuous-assignment subset required by the laboratory.
Supported logic operators are &, |, ^, and ~.
The simulator does not implement procedural always blocks, sequential logic, clocked behavior, delays, or complete Verilog scheduling semantics.
Four-state X/Z simulation is not implemented; signal values are treated as single-bit 0/1 values.
Icarus Verilog is not part of the Python simulation engine and is only an optional reference-verification tool.



