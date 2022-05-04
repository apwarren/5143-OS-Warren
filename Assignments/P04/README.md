### 4 May 2022
### 5143 Simulating Race Conditions

#### Group Members

- Allyson Warren

#### Overview:
This is a project written in python that implements a simulation
in which a given number of processes will try to perform their own
unique set of instructions and write to memory. This program assumes
only one cpu is available to allow a process to run and it will perfrom
using round robin scheduling. The program will also create privileged instructions
intertwined within all of the processes. Each privileged instruction has its own
unique id that tells when it can be run. Starting from 0, each privileged instruction
is to be given priority and cannot be preempted until finished with the instruction. 
If a process contains a privileged instruction but the one before has not run yet, the
process must wait until its previous one has ran. It will be stuck until then. While, waiting
other non-privileged instructions can run and will do a standard round robin scheduling. A
process also contains sleep commands intertwined within its instructions. If it gets called to 
sleep, then it must wait for that many clock ticks before it can go back into the ready queue
and have its next instruction be executed. While running, the simulation will display is progress
using the rich library. It will display the current content's of the memory as well as the following:
the Process currently on the cpu, the next upcoming privileged instruction needed, which processes 
cannot run until the upcoming privileged instruction has been ran, and what instructions are currently
sleeping.


#### Instructions

To run the simulation you will need to state the number of processes and instructions you want
to run for the simulation.

- To run type the following:
- python main.py 8


This will run the program with 8 processes that will all fight to get on the cpu and 
each will have intertwined privileged instructions between the 8 files.
