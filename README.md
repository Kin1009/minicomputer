# minicomputer
 This project is inspired from the game Turing Complete, level Calculations, but it's buffed.
# Help
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
or you could read my documentation.
# Files
app.py: The full kernel.
asm.py: The ASM version of the parser.
binary.py: The core version, only supports binary (1s and 0s type)