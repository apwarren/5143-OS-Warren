from alu import Alu
from lock import Lock
import sys

class Cpu():
    def __init__(self, registers, tslice, mem):
        self.cache = []
        self.pc = 0
        self.registers = registers
        self.alu = Alu(registers)
        self.timeSlice = tslice
        self.memory = mem
        self.lock = Lock()

    def loadProcess(self, pcb):
        instructions = pcb.getCurrentInstruction()
        counter = 0
        currentTSlice = self.timeSlice
        for instruction in instructions:
            if(currentTSlice >= 0 or pcb.getPriority() >= 0):
                parts = instruction.split()
                if(pcb.getPriority() <= self.registers[3]):
                    self.lock.wait()
                    self.lock.acquire()
                    if(parts[0] == 'LOAD'):
                        #We are using the next load instruction
                        index = int(parts[-1][-1]) - 1
                        self.registers[index] = int(parts[1]) + 1
                    if(instruction == instructions[-1]):
                        self.lock.release()

                #Cannot use this privileged memory yet as we have one before it to do
                elif(pcb.getPriority() > self.registers[3] and pcb.getPriority() < 9999):
                    self.lock.wait()
                    pcb.setState('PriorityWait')
                    return pcb
                        
            
                if(parts[0] == 'READ'):
                    index = int(parts[-1][-1])
                    memLetter = parts[1][0]
                    location = parts[1][1:]
                    self.registers[index] = self.memory[memLetter][location]

                elif (parts[0] == 'WRITE'):
                    index = int(parts[-1][-1])
                    memLetter = parts[-1][0]
                    location = parts[-1][1:]
                    self.memory[memLetter][location] = self.registers[index]

                elif():
                    index = int(parts[1][1])
                    print(index)
                    print(instruction)
                    self.registers[index] = self.alu.exec(parts[0])

                currentTSlice -= 1
                counter += 1


            elif(currentTSlice < 0):
                pcb.setPCounter(1, counter)
                pcb.setState('Ready')
                pcb.setRegContents(self.registers)
                print('Got cut off')
                sys.exit()
                return pcb
    
        pcb.finishedInstruction()
        if('sleep' in pcb.getCurrentInstruction()[0]):
            pcb.setState('Waiting')
            self.mainRegisters = self.registers
        else:
            pcb.setState('Ready')
        return pcb


    def getMemory(self):
        return self.memory

    def getRegContents(self):
        return self.registers         

    def getPriority(self):
        return self.registers[3]       

    def __str__(self):
        return f"[{self.registers}{self.alu}]"