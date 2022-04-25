import sys, json
from pcb import Pcb
from cpu import Cpu
from lock import Lock
from registers import Registers
from random import randint
from randInstructions import RandInstructions

Process = []    #List of all processes before they enter the queues
New = []
Ready = []
Waiting = []
PWaiting = []
Terminated = []
clock = 0
lock = Lock()
R4 = 0
try:
    processes = int(sys.argv[1])

finally:
    with open ('memory.json') as f:
        file = json.loads(f.read())

    timeSlice = randint(7,11)
    registers = Registers(4)
    Running = Cpu(registers, timeSlice, file)

    inst = RandInstructions(privilegedRatio=0.3, sleepRatio=0.15, numProcesses=processes)
    for i in range(processes):
        with open(f'program_{i}.txt', 'r') as f:
            instructions = json.loads(f.read())
        Process.append(Pcb(i, 'New', registers, instructions))


    for proc in Process:
        proc.setState('New')
        New.append(proc)

    #for i in range(50):
    while(len(Terminated) != processes):

        if(Ready != []):
            Running = Cpu(Ready[0].getRegContents(), timeSlice, file)
            Ready[0] = Running.loadProcess(Ready[0])
            file = Running.getMemory()
            if(Running.getPriority() > R4):
                R4 = Running.getPriority()

            if(Ready[0].getState() == 'Waiting'):
                sleeping = int(Ready[0].getCurrentInstruction()[0].split()[-1])
                Ready[0].setSleeper(sleeping)
                Waiting.append(Ready[0])
                del Ready[0]
            
            elif(Ready[0].getState() == 'Terminated'):
                Terminated.append(Ready[0])
                del Ready[0]
                print('terminate')
                print(Terminated[0])
                sys.exit()

            elif(Ready[0].getState() == 'PriorityWait'):
                PWaiting.append(Ready[0])
                del Ready[0]

            else:
                Ready[0].setState('Ready')
                Ready.append(Ready[0])
                del Ready[0]
               

        if(PWaiting != []):
            if(PWaiting[0].getPriority() == R4):
                PWaiting[0].setState('Ready')
                Ready.append(PWaiting[0])
                del PWaiting[0]
            PWaiting.sort(key=lambda x: x.getPriority())
            

        if(Waiting != []):
            for wait in range(len(Waiting)):
                if(Waiting[wait].showSleep() <= 1):
                    Waiting[wait].setSleeper(0)
                    print('Id:', Waiting[wait].getPid(), '  sleep:', Waiting[wait].showSleep())
                    Waiting[wait].finishedInstruction()
                    Waiting[wait].setState('Ready')
                    Ready.append(Waiting[wait])

                else:
                    Waiting[wait].sleep()

            Waiting = [i for i in Waiting if i.showSleep() != 0]
            

        Ready.sort(key=lambda x: x.getPriority())

        print('Ready\n',Ready)
        print('-----------')
        print('Waiting\n',Waiting)
        print('----------')
        print('PWaiting\n', PWaiting)
        print('----------------')

        print('Current Priority:', R4)

        for n in New:
            n.setState('Ready')
            Ready.append(n)
            New = []

