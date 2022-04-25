from rich import print
import json
import random
from random import shuffle
from randInstructions import randInstruction


def genMemory(sections=['A','B','C'],vals=[100,255,5],loadRandVals=True):
    mem = {}
    r = None
    start,stop,step = vals
    for section in sections:
        mem[section] = {}
        for i in range(start, stop, step):
            if loadRandVals:
                r = 0
            mem[section][i] = r

    return mem

if __name__ == "__main__":

    mem = genMemory()

    with open("memory.json", "w") as f:
        json.dump(mem, f, indent=2)
