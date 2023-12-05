import sys
from time import sleep
from random import random
from os import system
from os.path import exists, normpath
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Negative Terminal")
regs = {
    "0000": 0,
    "0001": 0,
    "0010": 0,
    "0011": 0,
    "0100": 0,
    "0101": 0,
    "0110": 0,
    "0111": 0,
    "1000": 0,
    "1001": 0,
    "1010": 0,
    "1011": 0,
    "1100": 0,
    "1101": 0,
    "1110": 0,
    "1111": 0,
}
def parse(bytes_=str):
    def split(text, part_length):
        return [text[i:i + part_length] for i in range(0, len(text), part_length)]
    bytes_ = split(bytes_, 16)
    index = 0
    while index < len(bytes_):
        byte = bytes_[index]
        opcode = byte[0:3]
        remain = byte[4:16]
        match opcode:
            case "000":
                pass
            case "001":
                regs[remain[0:4]] = int(f"0b{remain[5:12]}", base=0)
            case "010":
                print(regs[remain[0:4]])
            case "011":
                inp = input("Enter input as a number from 0 to 255: ")
                inp = int(inp)
                if inp not in list(range(0, 256, 1)):
                    print("Number not from 0 to 255")
                    inp = 0
                regs[remain[0:4]] = inp
            case "100":
                regs[remain[4:8]] = regs[remain[0:4]]
            case "101":
                regA = regs["0000"]
                regB = regs["0001"]
                match remain[0:3]:
                    case "000":
                        regs[3] = (regA + regB) % 256
                    case "001":
                        regs[3] = (regA - regB) % 256
                    case "010":
                        regs[3] = (regA * regB) % 256
                    case "011":
                        regs[3] = (regA / regB) % 256
                    case "100":
                        regs[3] = (regA ** regB) % 256
                    case "101":
                        regs[3] = (regA ** (1 / regB)) % 256
                    case _:
                        print("Invalid value: " + opcode)
            case "110":
                regA = regs["0000"]
                regB = regs["0001"]
                res = False
                match remain[0:3]:
                    case "000":
                        res = regA > regB
                    case "001":
                        res = regA < regB
                    case "010":
                        res = regA <= regB
                    case "011":
                        res = regA >= regB
                    case "100":
                        res = regA == regB
                    case "101":
                        res = regA != regB
                    case _:
                        print("Invalid value: " + opcode)
                if res:
                    byte__ = bytes_[index + 1]
                    parse(byte__)
                index += 1
            case "111":
                regA = regs["0000"]
                regB = regs["0001"]
                match remain[0:3]:
                    case "000":
                        regs[3] = (regA & regB) % 256
                    case "001":
                        regs[3] = (~regA) % 256
                    case "010":
                        regs[3] = (~(regA & regB)) % 256
                    case "011":
                        regs[3] = (regA | regB) % 256
                    case "100":
                        regs[3] = (~(regA | regB)) % 256
                    case "101":
                        regs[3] = (regA ^ regB) % 256
                    case "110":
                        regs[3] = (~(regA ^ regB)) % 256
                    case _:
                        print("Invalid value: " + opcode)
            case _:
                print("Invalid opcode: " + opcode)
        index += 1
def tobin(code=str):
    keys_ = {
    "imm": (lambda: "0" * 16),
    "cin": (lambda arg: f"0010{bin(int(arg[0]))[2:].zfill(4)}{bin(int(arg[1]))[2:].zfill(8)}"),
    "out": (lambda arg: f"0100{bin(int(arg[0]))[2:].zfill(4)}00000000"),
    "cun": (lambda arg: f"0110{bin(int(arg[0]))[2:].zfill(4)}00000000"),
    "cpy": (lambda arg: f"1000{bin(int(arg[0]))[2:].zfill(4)}{bin(int(arg[1]))[2:].zfill(4)}0000"),
    "mth": (lambda arg: f"1010{bin(int(arg[0]))[2:].zfill(3)}000000000"),
    "cnd": (lambda arg: f"1100{bin(int(arg[0]))[2:].zfill(3)}000000000{arg[1]}"),
    "log": (lambda arg: f"1110{bin(int(arg[0]))[2:].zfill(3)}000000000")
    }
    code = code.split(" ")
    command = code[0]
    res = keys_["imm"]() if command in ("imm", "") else keys_[command](code[1:])
    return res
def compile(code):
    res = ""
    for i in code.split("\n"):
        line = i.split(" ")
        if line[0] != "cnd":
            res += tobin(" ".join(line))
        else:
            res += tobin(" ".join(line[0:2]) + " " + tobin(" ".join(line[2:])))
    parse(res)
command = ""
multiline = False
if len(sys.argv) == 1: 
    print("Terminal version -1.0")
    sleep(random())
    print("Loading modules...")
    sleep(random())
    print("DETECTED: 16 registers -> 128 bit memory")
    keys = [
        "imm",
        "cin",
        "out",
        "cun",
        "cpy",
        "hlp",
        "prg",
        "run",
        "ext",
        "rst",
        "clr"
    ]
    for i in keys:
        sleep(random())
        print("LOADED: " + i)
    keys = ["mth", "cnd", "log"]
    for i in keys:
        sleep(random())
        print("LOADED: " + i)
    sleep(random())
    print("Loading...")
    sleep(1)
    print("READY. PRESS \"hlp\" TO GET HELP, \"ext\" TO EXIT, \"clr\" TO CLEAR SCREEN.")
elif len(sys.argv) in (2, 3):
    cmd = sys.argv[1]
    if cmd == "--noloading": pass
    elif exists(cmd):
        cmd = normpath(cmd)
        try:
            if len(sys.argv) == 3 and sys.argv[2] == "--noloading": pass
            else:
                print("Loading modules...")
                for i in range(17):
                    sleep(random())
                sleep(1)
            file = open(cmd, "r")
            file = file.read()
            compile(file)
            exit()
        except Exception as e:
            print("There's a problem with this file: " + str(e))
            exit()
else:
    print("Invalid argument.")
    exit()
while True:
    try:
        a = input("> ")
        if a == "prg":
            multiline = True
            command = ""
            while multiline:
                a = input(">> ")
                if a == "run":
                    compile(command)
                    multiline = False
                elif a == "ext":
                    exit()
                elif a == "clr":
                    system("cls")
                elif a == "rst":
                    command = ""
                else:
                    command += a + "\n"
            continue
        elif a == "hlp":
            print("""Help:
I'm lazy, so I'm going to explain in short python code.
imm [comment] -> #comment
cin [reg] [val] -> regs[reg] = val
cun [reg] -> regs[reg] = input()
out [reg] -> print(regs[reg])
cpy [reg] [dist] -> regs[dist] = regs[reg]
mth [opr] ->
    regA = regs[0]
    regB = regs[1]
    match opr:
        case 0:
            regs[3] = (regA + regB) % 256
        case 1:
            regs[3] = (regA - regB) % 256
        case 2:
            regs[3] = (regA * regB) % 256
        case 3:
            regs[3] = (regA / regB) % 256
        case 4:
            regs[3] = (regA ** regB) % 256
        case 5:
            regs[3] = (regA ** (1 / regB)) % 256 #root   
log [opr] ->
    regA = regs[0]
    regB = regs[1]
    match opr:
        case 0:
            regs[3] = (regA & regB) % 256
        case 1:
            regs[3] = (~regA) % 256
        case 2:
            regs[3] = (~(regA & regB)) % 256
        case 3:
            regs[3] = (regA | regB) % 256
        case 4:
            regs[3] = (~(regA | regB)) % 256
        case 5:
            regs[3] = (regA ^ regB) % 256
        case 6:
            regs[3] = (~(regA ^ regB)) % 256    
cnd [opr] [cmd] ->
    regA = regs[0]
    regB = regs[1]
    res = False
    match opr:
        case 0:
            res = regA > regB
        case 1:
            res = regA < regB
        case 2:
            res = regA <= regB
        case 3:
            res = regA >= regB
        case 4:
            res = regA == regB
        case 5:
            res = regA != regB
    if res:
        parse(cmd)
prg: start writing program
rst: reset program
run: run program, can be used multiple times in a row
hlp: show help
clr: clear screen (windows only)
ext: exit
    """)
        elif a == "run":
            compile(command)
        elif a == "clr":
            system("cls")
        elif a == "rst":
            command = ""
        elif a == "ext":
            exit()
        else:
            compile(a)
    except Exception as e:
        print("There is an error: " + str(e))