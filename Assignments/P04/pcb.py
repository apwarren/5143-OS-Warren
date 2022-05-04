from dis import Instruction
import sys

class Pcb():
    def __init__(self, id, state, regists, instructions):
        self.pid = id
        self.pState = state
        self.Priority = 9999
        self.regContents = regists
        self.instructions = instructions
        self.pCounter = [0, 0]
        self.currentInstruction = instructions[0]
        self.sleeper = 0


        if('p' in self.currentInstruction):
            self.Priority = int(self.currentInstruction[-1][1])
        #self.MemLimits = mem
        #self.openFiles = files
        #self.Devices = devices

    def setState(self, status):
        self.pState = status

    def getState(self):
        if(len(self.instructions) <= 0):
            return "Terminated"

        return self.pState

    def getPid(self):
        return self.pid

    def setRegContents(self, regs):
        self.regContents = regs

    def getRegContents(self):
        return self.regContents

    def getPriority(self):
        self.Priority = 9999

        if('LOAD' in "".join(self.currentInstruction)):
            for instruct in self.currentInstruction:
                instruct = instruct.split()
                if(instruct[0] == 'LOAD' and instruct[-1] == 'R4'):
                    self.Priority = int(instruct[1])
                    break
            
        return self.Priority

    def getCurrentInstruction(self):
        return self.currentInstruction

    def setPCounter(self, index, val):
        self.pCounter[index] = val
        self.currentInstruction = self.currentInstruction[val:]
        if(self.currentInstruction == []):
            self.finishedInstruction()
        

    def finishedInstruction(self):
        self.pCounter[0] += 1
        self.pCounter[1] = 0
        del self.instructions[0]
        if(len(self.instructions) > 0):
            self.currentInstruction = self.instructions[0]

    def sleep(self):
        self.sleeper -= 1

    def setSleeper(self, sheep):
        self.sleeper = sheep

    def showSleep(self):
        return self.sleeper

    def __repr__(self) -> str:
        return f"ID: {self.pid},\n State: {self.pState},\n Priority: {self.Priority},\n Current Instruction: {self.currentInstruction}\n\n"
