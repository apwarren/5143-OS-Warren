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

layout2.split(
    Layout(name = 'clock', size = 1),
    Layout(name = 'cpu'),
    Layout(name = 'io'),
    Layout(name = 'terminated', size = 4),
    Layout(name = 'results'),

)

layout['cpu'].ratio = 1
layout['io'].ratio = 1
layout['new'].ratio = 1
layout['ready'].ratio = 1
layout['waiting'].ratio = 1
layout['terminated'].ratio = 1

layout2['cpu'].ratio = 1
layout2['io'].ratio = 1
layout2['terminated'].ratio = 1
layout2['results'].ratio = 1


K = Clock()
timeSlice = 0

#From the command line, get the following:
algorithm = sys.argv[1]          #What scheduling algorithm to use
if(algorithm == 'RR'):         
    timeSlice = int(sys.argv[2]) #Get time slice value if round robin
    del sys.argv[2]     

cpuSize = int(sys.argv[2])       #How many cpus we will simulate in a run
ioSize = int(sys.argv[3])        #How many io devices used in a run
file = sys.argv[4]               #What file to read input from for run

with open(file) as f:
    Lines = f.readlines()

NewQ = Buffer(sized=len(Lines), Title='New')
ReadyQ = Buffer(sized=len(Lines), Title='Ready')
WaitingQ = Buffer(sized=len(Lines), Title='Waiting')
TerminatedQ = Buffer(sized=len(Lines), Title='Terminated', Reversed=True)

Process = []    #List of all processes before they enter the queues
New = []
Ready = []
Running = [None] * cpuSize
UsingIO = [None] * ioSize
Waiting = []
Terminated = []


CpuQ = Cpu(Running)
ioQ = IO(UsingIO)

clock = 0

for line in Lines:
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

layout2['clock'].update(K)
layout2['cpu'].update(CpuQ)
layout2['io'].update(ioQ)
layout2['terminated'].update(TerminatedQ)


with Live(layout, screen=True, redirect_stderr=False, refresh_per_second=2000) as live:
    try:
        #keep going until all processes have been completed
        while(len(Lines) > len(Terminated)):
            if(algorithm == 'RR'):
                for slice in range(len(currentSlice)):
                    currentSlice[slice] %= timeSlice

            for new in New:
                new.incrCPUWait()
                NewQ.decrease_buffer()
                ReadyQ.increase_buffer()
                Ready.append(new)

            New = []

            index = 0
            for process in Process:
                if(clock == process.getAT()):
                    New.append(process)
                    NewQ.increase_buffer()
                    index += 1
                else:
                    Process = Process[index:]
                    break

            for run in range(len(Running)):
                if(Running[run] is not None):
                    if(Running[run].getCPUBurst() == 0):
                        if(Running[run].getIOBurst() is None):
                            Running[run].setTAT(clock)
                            Terminated.append(Running[run])
                            TerminatedQ.increase_buffer()
                        else:
                            Running[run].nextCPUBurst()
                            Waiting.append(Running[run])
                            WaitingQ.increase_buffer()

                        Running[run] = None

                        if(algorithm == 'RR'):
                            currentSlice[run] = 0

                    elif(algorithm == 'RR' and currentSlice[run] == 0):
                        Ready.append(Running[run])
                        Running[run] = Ready[0]
                        del Ready[0]

                    else:
                        Running[run].decrementCpuBurst()
                        #Check if there is no new higher priorities
                        if(algorithm == 'PB'):
                            if(Ready != [] and Ready[0].getPriority() < Running[run].getPriority()):
                                Ready.append(Running[run])
                                Running[run] = Ready[0]
                                del Ready[0]
                                Ready.sort(key=lambda x: x.getPriority(), reverse=True)

                        elif(algorithm == 'SRT'):
                            if(Ready != [] and Ready[0].getTotalCPUTime() < Running[run].getTotalCPUTime()):
                                Ready.append(Running[run])
                                Running[run] = Ready[0]
                                del Ready[0]
                                Ready.sort(key=lambda x: x.getTotalCPUTime())
                else:
                    if(Ready != []):
                        ReadyQ.decrease_buffer()
                        Running[run] = Ready[0]
                        del Ready[0]

            for io in range(len(UsingIO)):
                if(UsingIO[io] is not None):
                    if(UsingIO[io].getIOBurst() == 0):
                        UsingIO[io].nextIOBurst()
                        Ready.append(UsingIO[io])
                        ReadyQ.increase_buffer()
                        if(Waiting != []):
                            WaitingQ.decrease_buffer()
                            UsingIO[io] = Waiting[0]
                            del Waiting[0]
                        else:
                            UsingIO[io] = None
                    else:
                        UsingIO[io].decrementIOBurst()
                else:
                    if(Waiting != []):
                        WaitingQ.decrease_buffer()
                        UsingIO[io] = Waiting[0]
                        del Waiting[0]

            for ready in Ready:
                ready.incrCPUWait()
                    
            for waiting in Waiting:
                waiting.incrIOWait()

            if(algorithm == 'PB'):
                Ready.sort(key=lambda x: x.getPriority(), reverse=True)

            elif(algorithm == 'SJF' or algorithm == 'SRT'):
                Ready.sort(key=lambda x: x.getTotalCPUTime())

            elif(algorithm == 'RR'):
                for slice in range(len(currentSlice)):
                    currentSlice[slice] += 1

            clock += 1
            K.addTime()
            CpuQ = Cpu(Running)
            ioQ = IO(UsingIO)

            sleep(0.001)

    except KeyboardInterrupt:
        pass


R = results(f=Terminated[:3], l=Terminated[-3:])
layout2['results'].update(R)

with Live(layout2, screen=True, redirect_stderr=False) as live:
    try:
        while(True):
            sleep(0)

    except KeyboardInterrupt:
        pass