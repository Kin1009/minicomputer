import binary
def tobin(code=str):
    code = code.split(" ")
    command = code[0]
    res = keys[command]() if command == "imm" else keys[command](code[1:])
    return res
keys = {
    "imm": lambda: "0000000000000000",
    "cin": lambda arg: f"0010{bin(int(arg[0]))[2:].zfill(4)}{bin(int(arg[1]))[2:].zfill(8)}",
    "out": lambda arg: f"0100{bin(int(arg[0]))[2:].zfill(4)}00000000",
    "cun": lambda arg: f"0110{bin(int(arg[0]))[2:].zfill(4)}00000000",
    "cpy": lambda arg: f"1000{bin(int(arg[0]))[2:].zfill(4)}{bin(int(arg[1]))[2:].zfill(8)}0000",
    "mth": lambda arg: f"1010{bin(int(arg[0]))[2:].zfill(3)}000000000",
    "cnd": lambda arg: f"1100{bin(int(arg[0]))[2:].zfill(3)}000000000{arg[1]}",
    "log": lambda arg: f"1110{bin(int(arg[0]))[2:].zfill(3)}000000000"
}
def compile(code):
    res = ""
    for i in code.split("\n"):
        line = i.split(" ")
        if line[0] != "cnd":
            res += tobin(" ".join(line))
        else:
            res += tobin(" ".join(line[0:2]) + " " + tobin(" ".join(line[2:])))
    binary.parse(res)