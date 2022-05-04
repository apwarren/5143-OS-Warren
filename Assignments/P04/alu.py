from random import randint
from decimal import Decimal

def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    if(r != 0):
        return l // r
    else: 
        return l


class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def exec(self, op, registers):
        self.lhs = int(registers[0])
        self.rhs = int(registers[1])
        self.op = op.upper()
        ans = Decimal(self.ops[self.op](self.lhs, self.rhs))
        if(ans > 9223372036854775807 or ans < -9223372036854775808):
            ans = randint(0,9)
        return ans

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"
