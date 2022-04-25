from random import shuffle, randint

def randInstruction(asList = False, sectioned = False):
    instruct = []
    for instruction in range(randint(100,999)):
        #singleBlock = [True, False]
        choices = ["MOV", "ADD", "SUB", "MUL", "DIV", "SET"]
        registers = ["R1", "R2"]
        memblocks = ["A", "B", "C"]
        memaddress = [x for x in range(100, 255, 5)]

        #shuffle(singleBlock)
        shuffle(choices)
        shuffle(registers)
        shuffle(memblocks)
        shuffle(memaddress)

        itype = choices[0]
        if(itype == 'SET'):
            r1 = registers[0]
            r2 = randint(0,9)
        else:
            r1, r2 = registers[:2]

        if(sectioned == True):
        #About 1/3  of the instructions will be sectioned to a specific memory block
            if(randint(0,20) >= 4):
                mb1 = mb2 = memblocks[0]
            else:
                mb1, mb2 = memblocks[:2]

        else:
            mb1, mb2 = memblocks[:2]

        madd1, madd2 = memaddress[:2]

        if not asList:
            instruct.append(f"READ {mb1}{madd1} {r1}\n")
            instruct[-1] += f"READ {mb2}{madd2} {r2}\n"
            instruct[-1] += f"{itype} {r1} {r2}\n"
            instruct[-1] += f"WRITE {r1} {mb1}{madd1}\n"
        else:
            inst = []
            inst.append(f"READ {mb1}{madd1} {r1}")
            inst.append(f"READ {mb2}{madd2} {r2}")
            inst.append(f"{itype} {r1} {r2}")
            inst.append(f"WRITE {r1} {mb1}{madd1}")
            instruct.append(inst)

    
    return instruct

def readInstruction(asList = False, sectioned = False):
    instruct = []
    for instruction in range(randint(100,200)):
        registers = ["R1", "R2"]
        memblocks = ["A", "B", "C"]
        memaddress = [x for x in range(100, 255, 5)]

        shuffle(registers)
        shuffle(memblocks)
        shuffle(memaddress)
        r1, r2 = registers[:2]

        if(sectioned == True):
        #About 1/3  of the instructions will be sectioned to a specific memory block
            if(randint(0,20) >= 4):
                mb1 = mb2 = memblocks[0]
            else:
                mb1, mb2 = memblocks[:2]

        else:
            mb1, mb2 = memblocks[:2]

        madd1, madd2 = memaddress[:2]

        if not asList:
            instruct.append(f"READ {mb1}{madd1} {r1}\n")
            instruct[-1] += f"READ {mb2}{madd2} {r2}\n"
            instruct[-1] += f"READ {mb1}{madd2} {r2}\n"
            instruct[-1] += f"READ {mb2}{madd1} {r1}\n"
        else:
            inst = []
            inst.append(f"READ {mb1}{madd1} {r1}")
            inst.append(f"READ {mb2}{madd2} {r2}")
            inst.append(f"READ {mb1}{madd2} {r2}")
            inst.append(f"READ {mb2}{madd1} {r1}")
            instruct.append(inst)

    
    return instruct

if __name__ == '__main__':

    print(randInstruction(True, True))