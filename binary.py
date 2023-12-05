import sys
args = sys.argv
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
# 8 bit not possible, 16-bit ins!
# 000 imm
# 001 copy from input
# 010 copy to output
# 011 copy from user input
# 100 copy
# 101 math
# 110 condition
# 111 logic
# 0000 0000 0000 0000
# 0010 [reg] [inp]
# 0100 [reg] 0000 0000
# 0110 [reg] 0000 0000
# 1000 [reg] [dist] 0000
# 1010 [ins]0 0000 0000
# 1100 [ins]0 0000 0000 [command]
# 1110 [ins]0 0000 0000
# 2 bytes each ins 4 bytes each condition
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
            case "001":
                regs[remain[0:4]] = int(f"0b{remain[5:12]}", base=0)
            case "010":
                print(regs[remain[0:4]])
            case "011":
                inp = input("Enter input as a number from 0 to 255: ")
                inp = int(inp)
                if inp not in list(range(0, 256, 1)):
                    raise ValueError("Number not from 0 to 255")
                regs[remain[0:4]] = inp
            case "100":
                regs[remain[4:8]] = regs[remain[0:4]]
            case "101":
                regA = regs["0000"]
                regB = regs["0001"]
                match remain[0:3]:
                    case "000":
                        regs["0010"] = (regA + regB) % 256
                    case "001":
                        regs["0010"] = (regA - regB) % 256
                    case "010":
                        regs["0010"] = (regA * regB) % 256
                    case "011":
                        regs["0010"] = (regA / regB) % 256
                    case "100":
                        regs["0010"] = (regA ** regB) % 256
                    case "101":
                        regs["0010"] = (regA ** (1 / regB)) % 256
                    case _:
                        raise ValueError("Invalid value: " + opcode)
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
                        raise ValueError("Invalid value: " + opcode)
                if res:
                    byte__ = bytes_[index + 1]
                    parse(byte__)
                index += 1
            case "111":
                regA = regs["0000"]
                regB = regs["0001"]
                match remain[0:3]:
                    case "000":
                        regs["0010"] = (regA & regB) % 256
                    case "001":
                        regs["0010"] = (~regA) % 256
                    case "010":
                        regs["0010"] = (~(regA & regB)) % 256
                    case "011":
                        regs["0010"] = (regA | regB) % 256
                    case "100":
                        regs["0010"] = (~(regA | regB)) % 256
                    case "101":
                        regs["0010"] = (regA ^ regB) % 256
                    case "110":
                        regs["0010"] = (~(regA ^ regB)) % 256
                    case _:
                        raise ValueError("Invalid value: " + opcode)
            case _:
                raise ValueError("Invalid opcode: " + opcode)
        index += 1