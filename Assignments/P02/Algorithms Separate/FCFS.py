from Pcb import pcb

class FCFS():
    def __init__(self, File, cpu = 1, io = 1):
        self.file = File
        self.cpuSize = cpu
        self.ioSize = io

    def run(self):
        with open(self.file) as f:
            Lines = f.readlines()

        Process = []    #List of all processes before they enter the queues
        New = []
        Ready = []
        Running = [None] * self.cpuSize
        UsingIO = [None] * self.ioSize
        Waiting = []
        Terminated = []

        clock = 0

        for line in Lines:
            Process.append(pcb(line))


        #keep going until all processes have been completed
        while(len(Lines) > len(Terminated)):
            for new in New:
                new.incrCPUWait()
                Ready.append(new)

            New = []

            index = 0
            for process in Process:
                if(clock == process.getAT()):
                    New.append(process)
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
                        else:
                            Running[run].nextCPUBurst()
                            Waiting.append(Running[run])

                        Running[run] = None
                    else:
                        Running[run].decrementCpuBurst()
                else:
                    if(Ready != []):
                        Running[run] = Ready[0]
                        del Ready[0]

            for io in range(len(UsingIO)):
                if(UsingIO[io] is not None):
                    if(UsingIO[io].getIOBurst() == 0):
                        UsingIO[io].nextIOBurst()
                        Ready.append(UsingIO[io])
                        if(Waiting != []):
                            UsingIO[io] = Waiting[0]
                            del Waiting[0]
                        else:
                            UsingIO[io] = None
                    else:
                        UsingIO[io].decrementIOBurst()
                        UsingIO[io].incrIOWait()
                else:
                    if(Waiting != []):
                        UsingIO[io] = Waiting[0]
                        del Waiting[0]

            for ready in Ready:
                ready.incrCPUWait()
                    
            for waiting in Waiting:
                waiting.incrIOWait()

            clock += 1


        print("new",New)
        print('ready',Ready)
        print('running',Running)
        print('io',UsingIO)
        print('waiting',Waiting)
        print('terminated',Terminated)
        print('\n')

        for term in Terminated:
            print(term.getAT())

if __name__ == "__main__":
    test = FCFS('test.dat')
    test.run()