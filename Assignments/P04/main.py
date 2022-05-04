import sys, json

from numpy import true_divide
from pcb import Pcb
from cpu import Cpu
from lock import Lock
from registers import Registers
from random import randint
'--------------------------------------------'
from randInstructions import RandInstructions
from time import sleep
'-----------------------------------------'
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
'----------------------------------------'
from createTable import memTable
from Clock import Clock
from onCPU import onCPU
from nextReg import nextPriv
from PWaiting import PWaitTable
from sleeping import Sleepers


console = Console()
layout = Layout()   #Display simulation as processes go through

layout.split(
    Layout(name="clock", size = 1),
    Layout(name= 'Rest'),
)

layout['Rest'].split(
    Layout(name="Memory", ratio= 8),
    Layout(name="Details", ratio=1),
    direction= 'horizontal'
    
)

layout["Details"].split(
    Layout(name="onCPU"), 
    Layout(name="nextPrivileged"),
    Layout(name="WaitingonPrivileged"),
    Layout(name="Sleeping"),
    direction= 'vertical'
)


layout['Memory'].ratio = 1
layout['onCPU'].ratio = 1
layout['nextPrivileged'].ratio = 1
layout['WaitingonPrivileged'].ratio = 1
layout['Sleeping'].ratio = 1

K = Clock()
On = onCPU('None')

Process = []    #List of all processes before they enter the queues
New = []
Ready = []
Waiting = []
PWaiting = []
Terminated = []
clock = 0
lock = Lock()
R4 = 0

nextP = nextPriv(R4)
pWaiters = PWaitTable(PWaiting)
sheep = Sleepers(Waiting)

try:
    processes = int(sys.argv[1])

finally:
    with open('memory.json') as f:
        file = json.loads(f.read())

    memDisplay = memTable(file)
    layout['Memory'].update(memDisplay)
    layout['clock'].update(K)
    layout['onCPU'].update(On)
    layout['nextPrivileged'].update(nextP)
    layout['WaitingonPrivileged'].update(pWaiters)
    layout['Sleeping'].update(sheep)


    #Generate a time slice that is between 7-11 clock ticks
    timeSlice = randint(7,11)

    #There will always be four registers
    registers = Registers(4)

    #Create a Cpu that each process is to run on
    Running = Cpu(registers, timeSlice, file)

    inst = RandInstructions(privilegedRatio=0.3, sleepRatio=0.15, numProcesses=processes)

    for i in range(processes):
        with open(f'program_{i}.txt', 'r') as f:
            instructions = json.loads(f.read())
        Process.append(Pcb(i, 'New', registers, instructions))

    #All processes are entering at the same time so all go to the new queue
    for proc in Process:
        proc.setState('New')
        New.append(proc)


    with Live(layout, screen=True, redirect_stderr=False, refresh_per_second=2000) as live:
        try:
            #Keep going until all processes have finished
            while(len(Terminated) != processes):
                
                #There are processes in the ready queue
                if(Ready != []):

                    #Cpu needs to be update with new register contents and memory
                    Running = Cpu(Ready[0].getRegContents(), timeSlice, file)

                    #First process in ready queue can use the cpu
                    Ready[0] = Running.loadProcess(Ready[0])

                    #update memory
                    file = Running.getMemory()

                    #If a privileged instruction was ran just now
                    if(Running.getPriority() > R4):
                        #Move on to the next privileged instruction
                        R4 = Running.getPriority()

                    #Process's next command is to sleep
                    if(Ready[0].getState() == 'Waiting'):
                        #Set up sleeping and then add process to the waiting queue
                        sleeping = int(Ready[0].getCurrentInstruction()[0].split()[-1])
                        Ready[0].setSleeper(sleeping)
                        Waiting.append(Ready[0])
                        del Ready[0]
                    
                    #Process is finished running all of its instrutions
                    elif(Ready[0].getState() == 'Terminated'):
                        Terminated.append(Ready[0])
                        del Ready[0]

                    #Process next instruction is privileged but not the upcoming one yet
                    elif(Ready[0].getState() == 'PriorityWait'):
                        PWaiting.append(Ready[0])
                        del Ready[0]

                    #Process can go back into ready to be read again later
                    else:
                        Ready[0].setState('Ready')
                        Ready.append(Ready[0])
                        del Ready[0]

                #Some privileged instructions are waiting for previous one to be ran
                if(PWaiting != []):

                    #The next privileged instruction can now be ran
                    if(PWaiting[0].getPriority() == R4):

                        #Add instruction to the ready queue to be ran
                        PWaiting[0].setState('Ready')
                        Ready.append(PWaiting[0])
                        del PWaiting[0]

                    #Sort privileged waiting queue by smallest priority
                    PWaiting.sort(key=lambda x: x.getPriority())
                    
                #Some processes are currently sleeping
                if(Waiting != []):
                    for wait in range(len(Waiting)):
                        #Process is done sleeping
                        if(Waiting[wait].showSleep() <= 1):
                            Waiting[wait].setSleeper(0)
                            Waiting[wait].finishedInstruction()

                            #Put process back into ready queue to begin running again
                            Waiting[wait].setState('Ready')
                            if(Waiting[wait].getState() == 'Ready'):
                                Ready.append(Waiting[wait])

                            ##Process is done running and can be terminated
                            elif(Waiting[wait].getState() == 'Terminated'):
                                Terminated.append(Waiting[wait])
                            
                        #Let process sleep for another clock tick
                        else:
                            Waiting[wait].sleep()

                    #Get rid of all sleeping processes that are done sleeping
                    Waiting = [i for i in Waiting if i.showSleep() != 0]
                    
                #Sort based on smallest priority. Non-privileged instructions get shoved to the back
                Ready.sort(key=lambda x: x.getPriority())

                #Create table displays to show progress to the terminal
                On = onCPU(f'P{Ready[0].getPid()}') if Ready != [] else onCPU('---')
                layout['onCPU'].update(On)
                nextP = nextPriv(R4)
                layout['nextPrivileged'].update(nextP)
                pWaiters = PWaitTable(PWaiting)
                layout['WaitingonPrivileged'].update(pWaiters)
                sheep = Sleepers(Waiting)
                layout['Sleeping'].update(sheep)

                #Increment time simulation has ran
                K.addTime()


                #Move all processes into the ready queue immediately
                for n in New:
                    n.setState('Ready')
                    Ready.append(n)
                    New = []
                
                #Pause after each clock tick to prevent simulation from running too fast
                sleep(.0001)

            while(True):
                pass
        
        except KeyboardInterrupt:
            with open('memory.json', 'w') as f:
                json.dump(file, f, indent=2)


