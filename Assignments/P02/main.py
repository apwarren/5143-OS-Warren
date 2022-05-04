from time import sleep
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
import sys
'--------------------------------------'
from Pcb import pcb
from Buffer import Buffer
from Clock import Clock
from CPU import Cpu
from IO import IO
from Results import results

console = Console()
layout = Layout()   #Display burst simulation as processes go through
layout2 = Layout()  #Display end results of simulation after everything finishes

#Create Two layouts, one for the cpu and io. The other for all buffer queues
layout.split(
    Layout(name="clock", size = 1),
    Layout(name="devices"),
    Layout(name="queues"),
)

layout["devices"].split(
    Layout(name="cpu"), 
    Layout(name="io"),
)

layout["queues"].split(
    Layout(name = 'new'),
    Layout(name = 'ready'),
    Layout(name = 'waiting'),
    Layout(name = 'terminated'),
)

'-------------------------------------------------'
layout2.split(
    Layout(name = 'clock', size = 1),
    Layout(name = 'cpu'),
    Layout(name = 'io'),
    Layout(name = 'terminated', size = 4),
    Layout(name = 'results'),

)

#Each layout should have equal sizing except the clock which should be minimal
layout['cpu'].ratio = 1
layout['io'].ratio = 1
layout['new'].ratio = 1
layout['ready'].ratio = 1
layout['waiting'].ratio = 1
layout['terminated'].ratio = 1
'------------------------------------------'
layout2['cpu'].ratio = 1
layout2['io'].ratio = 1
layout2['terminated'].ratio = 1
layout2['results'].ratio = 1


K = Clock()     #Simulation Clock
timeSlice = 0   #No time slicing unless specified

#From the command line, get the following:
algorithm = sys.argv[1]          #What scheduling algorithm to use
if(algorithm == 'RR'):         
    timeSlice = int(sys.argv[2]) #Get time slice value if round robin
    del sys.argv[2]     

cpuSize = int(sys.argv[2])       #How many cpus we will simulate in a run
ioSize = int(sys.argv[3])        #How many io devices used in a run
file = sys.argv[4]               #What file to read input from for run

with open(file) as f:            #Get all of the process to be read in list format
    Lines = f.readlines()

#All buffers displayed
NewQ = Buffer(sized=len(Lines), Title='New')
ReadyQ = Buffer(sized=len(Lines), Title='Ready')
WaitingQ = Buffer(sized=len(Lines), Title='Waiting')
TerminatedQ = Buffer(sized=len(Lines), Title='Terminated', Reversed=True)


Process = []                    #List of all processes before they enter the queues
New = []                        #List of all processes just entering the simulation
Ready = []                      #List of all processes waiting to access a cpu
Running = [None] * cpuSize      #List of all cpus available for processes to access
UsingIO = [None] * ioSize       #List of all io devices available for processes to access
Waiting = []                    #List of all processes waiting to access an io device
Terminated = []                 #List of all processes finished running and are done.


CpuQ = Cpu(Running)             #Display CPU table
ioQ = IO(UsingIO)               #Display IO table

clock = 0                       #Clock starts at 0

for line in Lines:              #Make each line its own pcb
    Process.append(pcb(line))


#Time slicing is only for round robin algorithm
if(algorithm == 'RR'):
    currentSlice = [1] * cpuSize  #Each Process on CPU get own counter for slicing


layout['clock'].update(K)
layout['cpu'].update(CpuQ)
layout['io'].update(ioQ)
layout['new'].update(NewQ)
layout['ready'].update(ReadyQ)
layout['waiting'].update(WaitingQ)
layout['terminated'].update(TerminatedQ)
'----------------------------------------------'
layout2['clock'].update(K)
layout2['cpu'].update(CpuQ)
layout2['io'].update(ioQ)
layout2['terminated'].update(TerminatedQ)


with Live(layout, screen=True, redirect_stderr=False, refresh_per_second=2000) as live:
    try:
        #keep going until all processes have been completed
        while(len(Lines) > len(Terminated)):

            if(algorithm == 'RR'):                       #using round robin so set up time slicing
                for slice in range(len(currentSlice)):   #Current slice should be less than the overall slice
                    currentSlice[slice] %= timeSlice

            for new in New:                 #Anything in the new queue can now go into ready
                new.incrCPUWait()           #Pcb has had to wait one clock tick for cpu
                NewQ.decrease_buffer()      #New has one less item in it
                ReadyQ.increase_buffer()    #Ready has one more item in it
                Ready.append(new)           #Add pcb to ready queue

            New = []                        #Nothing should be in the new queue now
            index = 0                       #How many new processes are being added into new

            for process in Process:
                if(clock == process.getAT()): #Its time for a pcb to enter the simulation
                    New.append(process)       #Pcb goes to the new queue at first
                    NewQ.increase_buffer()    #New queue has one more item in it
                    index += 1         
                else:
                    Process = Process[index:] #Only keep the processes that aren't in the simulation yet.
                    break

            #Look at all process currently on a cpu
            for run in range(len(Running)):
                if(Running[run] is not None):                   #Item is already accessing cpu

                    if(Running[run].getCPUBurst() == 0):        #Item is finished with current cpu burst

                        if(Running[run].getIOBurst() is None):  #Item is finished and has no more io bursts
                            Running[run].setTAT(clock)          #Set the items turn around time cause its finished
                            Terminated.append(Running[run])     #Add item to the terminated queue
                            TerminatedQ.increase_buffer()       #One more item was added to the terminated queue

                        else:                                   #Item has another io bursts to run through

                            Running[run].nextCPUBurst()         #Move on and store the next cpu burst to run
                            Waiting.append(Running[run])        #Move pcb to the waiting queue 
                            WaitingQ.increase_buffer()          #One more item is in the waiting queue

                        Running[run] = None                     #Nothing is using the CPU now

                        if(algorithm == 'RR'):                  #If algorithm is RR, reset the index's currentSlice
                            currentSlice[run] = 0

                    #Round Robin Simulation is being scheduled and we are out of our time slice
                    elif(algorithm == 'RR' and currentSlice[run] == 0):

                        Ready.append(Running[run])      #Put pcb back into ready queue for preemption
                        Running[run] = Ready[0]         #Next available process can go on cpu now
                        del Ready[0]                    #Next available process is no longer in ready queue

                    #Current Process can stay on cpu
                    else:

                        Running[run].decrementCpuBurst()    #Finished another clock tick on cpu

                        #Check if there is no new higher priorities
                        if(algorithm == 'PB'):
                            if(Ready != [] and Ready[0].getPriority() < Running[run].getPriority()):

                                #Replace cpu's pcb with pch of higher priority
                                Ready.append(Running[run])
                                Running[run] = Ready[0]
                                del Ready[0]

                                #Resort ready by highest priority first
                                Ready.sort(key=lambda x: x.getPriority(), reverse=True)

                        #Check if there is no shorter pcb time remaining
                        elif(algorithm == 'SRT'):
                            if(Ready != [] and Ready[0].getTotalCPUTime() < Running[run].getTotalCPUTime()):

                                #Replace cpu's pcb with pcb that has shorter time remaining
                                Ready.append(Running[run])
                                Running[run] = Ready[0]
                                del Ready[0]

                                #Resort ready by shortest time first
                                Ready.sort(key=lambda x: x.getTotalCPUTime())

                #CPU is Empty
                else:
                    if(Ready != []):                #Ready has a process that can be run
                        ReadyQ.decrease_buffer()    #One less item is in the ready queue
                        Running[run] = Ready[0]     #Add the next item in ready to the available cpu
                        del Ready[0]                #Remove said item from the ready queue

            for io in range(len(UsingIO)):

                #There is a process using the current IO device
                if(UsingIO[io] is not None):

                    if(UsingIO[io].getIOBurst() == 0):  #Process is done using the IO device

                        UsingIO[io].nextIOBurst()       #Move on to the next IO Burst for later
                        Ready.append(UsingIO[io])       #Add process onto the ready queue cause it needs a cpu
                        ReadyQ.increase_buffer()        #One item is added to the ready queue

                        if(Waiting != []):              #There are processes in waiting

                            WaitingQ.decrease_buffer()  #One less item is in the waiting queue
                            UsingIO[io] = Waiting[0]    #Put the next available process onto the IO device
                            del Waiting[0]              #Remove said process from the waiting queue

                        else:                           #There are not any new processes waiting for the io
                            UsingIO[io] = None          #IO Device is emtpy

                    #Process is not finished using the IO device
                    else:
                        UsingIO[io].decrementIOBurst()  #Clock tick occured, so decrement io burst

                #The IO Device is Empty
                else:
                    if(Waiting != []):              #If there are items available in the waiting queue
                        WaitingQ.decrease_buffer()  #One less item in the waiting queue
                        UsingIO[io] = Waiting[0]    #Add next item waiting onto the io device
                        del Waiting[0]              #remove said item from the waiting queue

            #Clock tick occured while in the ready queue
            for ready in Ready:
                ready.incrCPUWait() #Process had to wait another tick to access cpu
                    
            #Clock tick occured while in the waiting queue
            for waiting in Waiting:
                waiting.incrIOWait() #Process had to wait another tick to access io device

            #Running Priority Based Simulation so sort by highest Priority
            if(algorithm == 'PB'):
                Ready.sort(key=lambda x: x.getPriority(), reverse=True)

            #Running Shortest Job First or Shortest Remaining Time Simulation
            elif(algorithm == 'SJF' or algorithm == 'SRT'):
                Ready.sort(key=lambda x: x.getTotalCPUTime())   #sort by shortest cpu time needed

            #Running round robin simulation so increment each cpu's time slice
            elif(algorithm == 'RR'):
                for slice in range(len(currentSlice)):
                    currentSlice[slice] += 1

            clock += 1          #One clock tick has occurred
            K.addTime()         #Add time to the display clock
            CpuQ = Cpu(Running) #Display new Cpu table
            ioQ = IO(UsingIO)   #Display new io table

            sleep(0.001)        #Pause so simulation doesn't end quickly

    except KeyboardInterrupt:
        pass


#Get results of finished simulation
#Get the first and last three finished processes
R = results(f=Terminated[:3], l=Terminated[-3:])
layout2['results'].update(R)

with Live(layout2, screen=True, redirect_stderr=False) as live:
    try:
        while(True):    #Display results until interrupted by keyboard
            sleep(0)

    except KeyboardInterrupt:
        pass