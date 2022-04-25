from random import randint, shuffle, random
import json, sys, time, os
import threading as thread
from randInstructions import randInstruction, readInstruction
from readingMem import readMem
from memoryDisplay import memDisplay
from rich import print_json, print, pretty
import pandas as pd


writerAmount = int(sys.argv[1])
try:
    if(sys.argv[2].lower() == 'yes' or sys.argv[2].lower == 'true'):
        sectionBlocks = True
    else:
        sectionBlocks = False
except Exception:
    sectionBlocks = False

with open('memory.json') as f:
    memory = json.load(f)

readers = readMem()
memD = memDisplay(memory)

class RWLock:
    
    """ A lock object that allows many simultaneous "read locks", but
  only one "write lock." """
    def __init__(self):
        self._read_readyA = thread.Condition(thread.RLock())
        self._read_readyB = thread.Condition(thread.RLock())
        self._read_readyC = thread.Condition(thread.RLock())

        self._readersA = 0
        self._readersB = 0
        self._readersC = 0

        self._writersA = 0
        self._writersB = 0
        self._writersC = 0
        
    def acquire_read(self, block = ''):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        if(block == 'A'):
            self._read_readyA.acquire()
            try:
                while self._writersA > 0:
                    self._read_readyA.wait()
                self._readersA += 1
            finally:
                self._read_readyA.release() 

        elif(block == 'B'):
            self._read_readyB.acquire()
            try:
                while self._writersB > 0:
                    self._read_readyB.wait()
                self._readersB += 1
            finally:
                self._read_readyB.release() 

        elif(block == 'C'):
            self._read_readyC.acquire()
            try:
                while self._writersC > 0:
                    self._read_readyC.wait()
                self._readersC += 1
            finally:
                self._read_readyC.release() 

        else:
            self._read_readyA.acquire()
            self._read_readyB.acquire()
            self._read_readyC.acquire()
            try:
                while self._writersA > 0:
                    self._read_readyA.wait()
                while self._writersB > 0:
                    self._read_readyB.wait()
                while self._writersC > 0:
                    self._read_readyC.wait()
                self._readersA += 1
                self._readersB += 1
                self._readersC += 1

            finally:
                self._read_readyA.release()
                self._read_readyB.release()
                self._read_readyC.release()
        #os.system('cls')
        #printMem()

    def release_read(self, block = ''):
        """ Release a read lock. """
        if(block == 'A'):
            self._read_readyA.acquire()
            try:
                self._readersA -= 1
                if not self._readersA:
                    self._read_readyA.notifyAll()
            finally:
                self._read_readyA.release()

        elif(block == 'B'):
            self._read_readyB.acquire()
            try:
                self._readersB -= 1
                if not self._readersB:
                    self._read_readyB.notifyAll()
            finally:
                self._read_readyB.release()

        elif(block == 'C'):
            self._read_readyC.acquire()
            try:
                self._readersC -= 1
                if not self._readersC:
                    self._read_readyC.notifyAll()
            finally:
                self._read_readyC.release()

        else:
            self._read_readyA.acquire()
            self._read_readyB.acquire()
            self._read_readyC.acquire()
            try:
                self._readersA -= 1
                if not self._readersA:
                    self._read_readyA.notifyAll()

                self._readersB -= 1
                if not self._readersB:
                    self._read_readyB.notifyAll()

                self._readersC -= 1
                if not self._readersC:
                    self._read_readyC.notifyAll()
            finally:
                self._read_readyA.release()
                self._read_readyB.release()
                self._read_readyC.release()
        #os.system('cls')
        #printMem()


    def acquire_write(self, block = ''):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        if(block == 'A'):
            self._read_readyA.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersA += 1
            while self._readersA > 0:
                self._read_readyA.wait()

        elif(block == 'B'):
            self._read_readyB.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersB += 1
            while self._readersB > 0:
                self._read_readyB.wait()

        elif(block == 'C'):
            self._read_readyC.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._writersC += 1
            while self._readersC > 0:
                self._read_readyC.wait()

        else:
            self._read_readyA.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._read_readyB.acquire()   # A re-entrant lock lets a thread re-acquire the lock
            self._read_readyC.acquire()   # A re-entrant lock lets a thread re-acquire the lock

            self._writersA += 1
            self._writersB += 1
            self._writersC += 1

            while self._readersA > 0:
                self._read_readyA.wait()

            while self._readersB > 0:
                self._read_readyB.wait()

            while self._readersC > 0:
                self._read_readyC.wait()

    def release_write(self, block = ''):
        """ Release a write lock. """
        if(block == 'A'):
            self._writersA -= 1
            self._read_readyA.notifyAll()
            self._read_readyA.release()

        elif(block == 'B'):
            self._writersB -= 1
            self._read_readyB.notifyAll()
            self._read_readyB.release()

        elif(block == 'C'):
            self._writersC -= 1
            self._read_readyC.notifyAll()
            self._read_readyC.release()

        else:
            self._writersA -= 1
            self._writersB -= 1
            self._writersC -= 1

            self._read_readyA.notifyAll()
            self._read_readyB.notifyAll()
            self._read_readyC.notifyAll()

            self._read_readyA.release()            
            self._read_readyB.release()
            self._read_readyC.release()
        #os.system('cls')
        #printMem()


class Writer():
    def __init__(self, rw_lock, file, sectioned = False):
        """
        @param memory: memory shared by the readers and writers
        @type memory_: dictionary
        @type rw_lock: L{RWLock}
        """
        self.__rw_lock = rw_lock
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
        for instruction in self.instructions:
            memBlock = 'All'
            instruction = instruction.split('\n')
            read1 = instruction[0].split()
            read2 = instruction[1].split()
            write = instruction[3].split()

            if(read1[1][0] == read2[1][0] and read1[1][0] == write[-1][0] and self.memSectioned == True):
                memBlock = read1[1][0]

            self.register[0] = memory[read1[1][0]][read1[1][1:]]
            self.register[1] = memory[read2[1][0]][read2[1][1:]]

            self.register[0] = operation(instruction[2], self.register)
            #Only lock writing when actually writing to memory
            inst4 = instruction[3].split()

            #Only prevent access for a specific memory block instruction is in one block
            time.sleep(random())
            self.__rw_lock.acquire_write(block = memBlock)

            print(f'Writer {self.id} is writing to {memBlock}')

            memory[inst4[-1][0]][inst4[-1][1:]] = self.register[0]

            self.__rw_lock.release_write(block = memBlock)
            time.sleep(random())
            print(f'Writer {self.id} is finished writing')

class Reader():
    def __init__(self, rw_lock, id, sectioned = False):
        """
        @param memory_: shared memory by readers and writers
        @type memory_: dictionary
        @type rw_lock: L{RWLock}
        """
        self.__rw_lock = rw_lock
        self.id = id
        """a copy of a the buffer read while in critical section"""    
        self.register = [0,0]

        if(sectioned == True):
            self.memSectioned = True
            self.instructions = readInstruction(False, True)
        else:
            self.memSectioned = False
            self.instructions = readInstruction()

        print(rw_lock)

    def run(self):
        for instruction in self.instructions:
            memBlock = 'All'
            instruction = instruction.split('\n')
            read1 = instruction[0].split()
            read2 = instruction[1].split()
            read3 = instruction[2].split()
            read4 = instruction[3].split()

            if(read1[0][1] == read2[0][1] and read2[0][1] == read3[0][1] and read3[0][1] == read4[0][1] and self.memSectioned == True):
                memBlock = read1[1][0]

            
            #Only prevent access for a specific memory block instruction is in one block
            time.sleep(random())
            self.__rw_lock.acquire_read(block = memBlock)

            print(f'Reader {self.id} is reading {memBlock}')
            self.register[0] = memory[read1[1][0]][read1[1][1:]]
            self.register[1] = memory[read2[1][0]][read2[1][1:]]
            self.register[1] = memory[read3[1][0]][read3[1][1:]]
            self.register[0] = memory[read4[1][0]][read4[1][1:]]


            self.__rw_lock.release_read(block = memBlock)

            time.sleep(random())
            print(f'Reader {self.id} is finished reading')

def operation(command, registers):
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

def printMem():
    df = pd.DataFrame.from_dict(memory, orient='index').reset_index(drop=True)
    df = df.transpose()
    df.rename(columns = {0:'A', 1:'B', 2: 'C'}, inplace = True)
    print(df)

if __name__ == "__main__":

    start_time = time.perf_counter()

    rw_lock = RWLock()
    threads = []

    #Generate as many file intstructions as writers
    for i in range(writerAmount):
        try:
            if(sys.argv[4].lower() == 'new'):
                with open(f'file{i}', 'w') as f:
                    f.write('\n'.join(randInstruction(False, True)))
        except:
            pass
        finally:
            if(sectionBlocks == True):
                threads.append(Writer(rw_lock, f'file{i}', True))
                #Create 5 times as many readers as writers
                threads.append(Reader(rw_lock, i * 5, True))
                threads.append(Reader(rw_lock, i * 5 + 1, True))
                threads.append(Reader(rw_lock, i * 5 + 2, True))
                threads.append(Reader(rw_lock, i * 5 + 3, True))
                threads.append(Reader(rw_lock, i * 5 + 4, True))

            else:
                threads.append(Writer(rw_lock, f'file{i}'))
                #Create 5 times as many readers as writers
                threads.append(Reader(rw_lock, i * 5))
                threads.append(Reader(rw_lock, i * 5 + 1))
                threads.append(Reader(rw_lock, i * 5 + 2))
                threads.append(Reader(rw_lock, i * 5 + 3))
                threads.append(Reader(rw_lock, i * 5 + 4))


    #shuffle(threads)

    for t in threads:
        t.run()
    sys.exit()
        #printMem()
        #os.system('cls')


    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # print stats
    print(execution_time, 'seconds')

    with open('memory.json', 'w') as f:
        json.dump(memory, f, indent=2)

