from random import randint, shuffle, random
import json, sys, time
import threading as thread
from randInstructions import randInstruction, readInstruction
'----------------------------------------'
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
'----------------------------------------'
from createTable import memTable
from readingMem import readMem
from writingMem import writeMem



console = Console()
layout = Layout()   #Display memory and memory accessors simulation as processes go through

layout.split(
    Layout(name="Memory"),
    Layout(name="Accessors", ratio=2),
    direction= 'horizontal'             #Split Vertically so memory has enough room
    
)


layout["Accessors"].split(
    Layout(name="Reading"), 
    Layout(name="Writing"),
    direction= 'vertical'
)


layout['Memory'].ratio = 1
layout['Reading'].ratio = 1
layout['Writing'].ratio = 1


writerAmount = int(sys.argv[1])
try:
    #We want memory to be sectioned off and not all blocked off at once
    if(sys.argv[2].lower() == 'yes' or sys.argv[2].lower == 'true'):
        sectionBlocks = True
    #We want all of memory to be blocked off if writing
    else:
        sectionBlocks = False

except Exception:
    #We want all of memory to be blocked off if writing
    sectionBlocks = False

#Access current memory to be read
with open('memory.json') as f:
    memory = json.load(f)

#Display memory as a table to the user
memDisplay = memTable(memory)

readingA = []   #list of readers reading A
readingB = []   #list of readers reading B
readingC = []   #list of readers reading C
writingA = ''   #Writing writing to A
writingB = ''   #Writing writing to B
writingC = ''   #Writing writing to C

#Display who is reading and writing to memory
reading = readMem(readingA, readingB, readingC)
writing = writeMem(writingA, writingB, writingC)

layout['Memory'].update(memDisplay)
layout['Reading'].update(reading)
layout['Writing'].update(writing)


class RWLock:
    
    """ A lock object that allows many simultaneous "read locks", but
        only one "write lock. Memory can locked all at once or in sections based
        on current simulation. """
    def __init__(self):
        self._read_readyA = thread.Condition(thread.RLock())
        self._read_readyB = thread.Condition(thread.RLock())
        self._read_readyC = thread.Condition(thread.RLock())

        self._readersA = 0  #No one is currently reading A
        self._readersB = 0  #No one is currently reading B
        self._readersC = 0  #No one is currently reading C

        self._writersA = 0  #No one is currently writing to A
        self._writersB = 0  #No one is currently writing to B
        self._writersC = 0  #No one is currently writing to C
        
    def acquire_read(self, block = ''):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        
        if(block == 'A'):                   #Reading only section A of memory
            self._read_readyA.acquire()     #Acquire lock for reading A
            time.sleep(.05)
            try:
                while self._writersA > 0:    #Cannot read until writing it done
                    self._read_readyA.wait() #Wait until writing is finished
                self._readersA += 1          #Currently reading A

            finally:
                self._read_readyA.release()  

        elif(block == 'B'):                   #Reading only section B of memory
            self._read_readyB.acquire()       #Acquire lock for reading B
            time.sleep(.05)
            try:
                while self._writersB > 0:    #Cannot read until writing it done
                    self._read_readyB.wait() #Wait until writing is finished
                self._readersB += 1          #Currently reading B
            finally:
                self._read_readyB.release() 

        elif(block == 'C'):                   #Reading only section C of memory
            self._read_readyC.acquire()       #Acquire lock for reading C
            time.sleep(.05)
            try:
                while self._writersC > 0:    #Cannot read until writing it done
                    self._read_readyC.wait() #Wait until writing is finished
                self._readersC += 1          #Currently reading C
            finally:
                self._read_readyC.release()

        else:   #Reading to all sections of memory
            try:
                self._read_readyA.acquire() #Access memory in A if no one is writing
                while (self._writersA > 0):
                    self._read_readyA.wait()
                self._readersA += 1

                self._read_readyB.acquire() #Access memory in B if no one is writing
                while(self._writersB > 0):
                    self._read_readyB.wait()
                self._readersB += 1

                self._read_readyC.acquire() #Access memory in C if no one is writing
                while(self._writersC > 0):
                    self._read_readyC.wait()
                self._readersC += 1
                time.sleep(.05)

            finally:
                self._read_readyA.release()
                self._read_readyB.release()
                self._read_readyC.release()
            

    def release_read(self, block = ''):
        """ Release a read lock. """

        if(block == 'A'):               #Done reading from A
            self._read_readyA.acquire()
            try:
                self._readersA -= 1
                if not self._readersA:
                    self._read_readyA.notifyAll()
            finally:
                self._read_readyA.release()

        elif(block == 'B'):             #Done reading from B
            self._read_readyB.acquire()
            try:
                self._readersB -= 1
                if not self._readersB:
                    self._read_readyB.notifyAll()
            finally:
                self._read_readyB.release()

        elif(block == 'C'):             #Done reading from C
            self._read_readyC.acquire()
            try:
                self._readersC -= 1
                if not self._readersC:
                    self._read_readyC.notifyAll()
            finally:
                self._read_readyC.release()

        else:                           #Done reading all of memory
            self._read_readyA.acquire()
            try:
                self._readersA -= 1
                if not self._readersA:
                    self._read_readyA.notifyAll()
            finally:
                self._read_readyA.release()

            self._read_readyB.acquire()
            try:
                self._readersB -= 1
                if not self._readersB:
                    self._read_readyB.notifyAll()
            finally:
                self._read_readyB.release()

            self._read_readyC.acquire()
            try:
                self._readersC -= 1
                if not self._readersC:
                    self._read_readyC.notifyAll()
            finally:
                self._read_readyC.release()



    def acquire_write(self, block = ''):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """

        if(block == 'A'):                 #Only block off memory in section A
            self._read_readyA.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersA += 1
            while self._readersA > 0:
                self._read_readyA.wait()

        elif(block == 'B'):               #Only block off memory in section B
            self._read_readyB.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersB += 1
            while self._readersB > 0:
                self._read_readyB.wait()

        elif(block == 'C'):               #Only block off memory in section C
            self._read_readyC.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersC += 1
            while self._readersC > 0:
                self._read_readyC.wait()

        else:                             #Block off all memory while writing
            self._read_readyA.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersA += 1
            while self._readersA > 0:
                self._read_readyA.wait()

            self._read_readyB.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersB += 1
            while self._readersB > 0:
                self._read_readyB.wait()

            self._read_readyC.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersC += 1
            while self._readersC > 0:
                self._read_readyC.wait()
            

    def release_write(self, block = ''):
        """ Release a write lock. """

        if(block == 'A'):                   #Done writing to section A
            self._writersA -= 1
            self._read_readyA.notifyAll()
            self._read_readyA.release()

        elif(block == 'B'):                 #Done writing to section B
            self._writersB -= 1
            self._read_readyB.notifyAll()
            self._read_readyB.release()

        elif(block == 'C'):                 #Done writing to section C
            self._writersC -= 1
            self._read_readyC.notifyAll()
            self._read_readyC.release()

        else:                               #Done writing to all of memory
            self._writersA -= 1
            self._read_readyA.notifyAll()
            self._read_readyA.release()

            self._writersB -= 1
            self._read_readyB.notifyAll()
            self._read_readyB.release()

            self._writersC -= 1
            self._read_readyC.notifyAll()
            self._read_readyC.release()
            


class Writer(thread.Thread):
    def __init__(self, rw_lock, file, sectioned = False):
        """
        Writer Class to write to memory
        rw_lock: L{RWLock}
        file    :   instructions to be read
        sectioned   :   whether to block all or only sections of memory
        """
        thread.Thread.__init__(self)

        self.__rw_lock = rw_lock    #All readers and writers have the same RWLock
        self.id = file[-1]
        #Two registers to perform operations on
        self.register = [0,0]

        #Generate 100-9,999 sets of instructions for writer to do
        with open(file) as f:
            l = f.read()
            l = l.split('\n\n')
        self.instructions = l

        self.memSectioned = sectioned

        
    def run(self):
        global memDisplay
        global writingA, writingB, writingC

        for instruction in self.instructions:
            memBlock = 'All'
            instruction = instruction.split('\n')
            read1 = instruction[0].split()
            read2 = instruction[1].split()
            write = instruction[3].split()

            #We are sectioning memory and a writer only needs one memory block
            if(read1[1][0] == read2[1][0] and read1[1][0] == write[-1][0] and self.memSectioned == True):
                memBlock = read1[1][0]

            #Only prevent access for a specific memory block instruction is in one block
            time.sleep(random())
            self.__rw_lock.acquire_write(block = memBlock)

            if (memBlock == 'A' or memBlock == 'All'):
                writingA = str(self.id)

            if (memBlock == 'B' or memBlock == 'All'):
                writingB = str(self.id)

            if (memBlock == 'C' or memBlock == 'All'):
                writingC = str(self.id)
                
            writing = writeMem(writingA, writingB, writingC)
            layout['Writing'].update(writing)
            time.sleep(1)

            self.register[0] = memory[read1[1][0]][read1[1][1:]]
            self.register[1] = memory[read2[1][0]][read2[1][1:]]

            self.register[0] = operation(instruction[2], self.register)
            #Only lock writing when actually writing to memory
            inst4 = instruction[3].split()

            memory[inst4[-1][0]][inst4[-1][1:]] = self.register[0]

            memDisplay = memTable(memory)

            #print(f'Writer {self.id} is finished writing to {memBlock}')
            self.__rw_lock.release_write(block = memBlock)
            if (memBlock == 'A' or memBlock == 'All'):
                writingA = ''

            if (memBlock == 'B' or memBlock == 'All'):
                writingB = ''

            if (memBlock == 'C' or memBlock == 'All'):
                writingC = ''
            
            writing = writeMem(writingA, writingB, writingC)
            layout['Memory'].update(memDisplay)
            layout['Writing'].update(writing)

            time.sleep(random())



class Reader(thread.Thread):
    def __init__(self, rw_lock, id, sectioned = False):
        """
        Reader Class for reading memory
        rw_lock: L{RWLock}
        id  :   unique id of a given reader
        sectioned   :   whether all or only sections of memory get blocked off at once
        """
        thread.Thread.__init__(self)
        self.__rw_lock = rw_lock
        self.id = id

        """Contents stored within the reader's registers"""    
        self.register = [0,0]

        #Generate reader instructions for reader to read from
        if(sectioned == True):
            self.memSectioned = True
            self.instructions = readInstruction(False, True)
        else:
            self.memSectioned = False
            self.instructions = readInstruction(False, False)

    def run(self):
        global memDisplay

        #Run through all of the reader's instructions
        for instruction in self.instructions:
            memBlock = 'All'    #Default is to block off all memory

            instruction = instruction.split('\n')
            read1 = instruction[0].split()
            read2 = instruction[1].split()
            read3 = instruction[2].split()
            read4 = instruction[3].split()

            #We are sectioning memory and a reader only needs one memory block
            if(read1[0][1] == read2[0][1] and read2[0][1] == read3[0][1] and read3[0][1] == read4[0][1] and self.memSectioned == True):
                memBlock = read1[1][0]

            
            #Only prevent access for a specific memory block instruction is in one block
            time.sleep(random())

            #Begin reading memory
            self.__rw_lock.acquire_read(block = memBlock)

            if (memBlock == 'A' or memBlock == 'All'):
                readingA.append(self.id)

            if (memBlock == 'B' or memBlock == 'All'):
                readingB.append(self.id)

            if (memBlock == 'C' or memBlock == 'All'):
                readingC.append(self.id)
                
            reading = readMem(readingA, readingB, readingC)
            layout['Reading'].update(reading)

            self.register[0] = memory[read1[1][0]][read1[1][1:]]
            self.register[1] = memory[read2[1][0]][read2[1][1:]]
            self.register[1] = memory[read3[1][0]][read3[1][1:]]
            self.register[0] = memory[read4[1][0]][read4[1][1:]]

            #Done reading memory
            self.__rw_lock.release_read(block = memBlock)


            if (memBlock == 'A' or memBlock == 'All'):
                try:
                    readingA.remove(self.id)
                except ValueError:
                    pass

            if (memBlock == 'B' or memBlock == 'All'):
                try:
                    readingB.remove(self.id)
                except ValueError:
                    pass
            if (memBlock == 'C' or memBlock == 'All'):
                try:
                    readingC.remove(self.id)
                except ValueError:
                    pass

            reading = readMem(readingA, readingB, readingC)
            layout['Reading'].update(reading)

            time.sleep(random())


def operation(command, registers):
    """Function to perform operation for writer class"""
    cmd = command.split()
    r1 = registers[0]
    r2 = registers[1]

    if(cmd[0] == 'MOV'):
        r1 = r2
    elif(cmd[0] == 'ADD'):
        r1 = r1 + r2
    elif(cmd[0] == 'SUB'):
        r1 = r1 - r2
    elif(cmd[0] == 'MUL'):
        r1 = r1 * r2
    elif(cmd[0] == 'DIV'):
        if(r2 != 0):
            r1 = r1 // r2
    else:
        r1 = int(cmd[-1])

    return r1



if __name__ == "__main__":

    #Time how long it takes for simulation to run
    start_time = time.perf_counter()

    rw_lock = RWLock()
    threads = []

    #Generate as many file intstructions as writers
    for i in range(writerAmount):
        try:
            if(sys.argv[-1].lower() == 'new'):
                with open(f'file{i}', 'w') as f:
                    f.write('\n'.join(randInstruction(False, True)))
        except:
            pass
        finally:
            #We want to section off memory
            if(sectionBlocks == True):
                threads.append(Writer(rw_lock, f'file{i}', True))
                #Create 5 times as many readers as writers
                threads.append(Reader(rw_lock, i * 5, True))
                threads.append(Reader(rw_lock, i * 5 + 1, True))
                threads.append(Reader(rw_lock, i * 5 + 2, True))
                threads.append(Reader(rw_lock, i * 5 + 3, True))
                threads.append(Reader(rw_lock, i * 5 + 4, True))

            #Treat memory as one single entity
            else:
                threads.append(Writer(rw_lock, f'file{i}', False))
                #Create 5 times as many readers as writers
                threads.append(Reader(rw_lock, i * 5, False))
                threads.append(Reader(rw_lock, i * 5 + 1, False))
                threads.append(Reader(rw_lock, i * 5 + 2, False))
                threads.append(Reader(rw_lock, i * 5 + 3, False))
                threads.append(Reader(rw_lock, i * 5 + 4, False))

    shuffle(threads)

    with Live(layout, screen=True, redirect_stderr=False, refresh_per_second=2000) as live:
        try:
            for t in threads:
                t.start()
            
            for t in threads:
                t.join()


            end_time = time.perf_counter()
            execution_time = end_time - start_time

            # print stats
            print(execution_time, 'seconds')

            with open('memory.json', 'w') as f:
                json.dump(memory, f, indent=2)

                
        except KeyboardInterrupt:
            pass

