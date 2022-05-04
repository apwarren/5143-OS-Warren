#### 4 May 2022
#### 5143 Scheduling Simulator

#### Group Members

- Allyson Warren

#### Overview:
This is a project written in python that implements 5 differnt scheduling 
algorithms. This program can simulate: First Come First Serve (FCFS), 
Shorest Remaining Time (SRT), Shortest Job First (SJF), Round Robin (RR),
 and Priority Based (PB). The simulation will be displayed using the 
 rich terminal library in which it will show the queues as buffers and
 the cpus and io devices in their own table.


## Scheduling Algorithms

#### First-Come-First-Serve, FCFS

- FCFS queues processes in the order that they arrive in the ready queue.
- This is a **non-preemptive** scheduling algorithm.

#### Shortest-Job-First, SJF

- SJF selects for execution the waiting process with the smallest execution time.
- SJF is a **non-preemptive** algorithm

#### Shortest-Remaining-Time, SRT

- SRT selects the process with the smallest amount of time remaining until completion is selected to execute. 
- SRT is a **preemptive version** of shortest job next scheduling. 

#### Priority-Based, PB

- PB assigns a fixed priority rank to every process, and the scheduler arranges the processes in the ready queue in order of their priority. 
- Lower-priority processes get interrupted by incoming higher-priority processes.
- This is a **preemptive scheduling** algorithm.

#### Round-Robin, RR

- RR assigns a time-slice or time-quantum, and cycles through each process equally. 
- If the process completes within that time-slice it gets terminated otherwise it is rescheduled after giving a chance to all other processes.
- This is a **preemptive scheduling** algorithm.

#### Instructions

To run the simulation you will need to state the scheduling type, amount of cpus and io devices desired,
and what data file you are reading from. For Round Robin you will also need to state the time quantum
after RR.

- To run type the following:
- python main.py FCFS 9 5 datafile.dat
- python main.py SRT 9 5 datafile.dat
- python main.py SJF 9 5 datafile.dat
- python main.py PB 9 5 datafile.dat
- python main.py RR 10 9 5 datafile.dat


This will run the desired simulation with 9 cpus and 5 io devices, It will also have a time quantum
of 10 for round robin. It will read the processes from datafile.dat

