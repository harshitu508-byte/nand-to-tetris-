#!/usr/bin/env python3
"""
assembler.py - Hack assembler (Nand to Tetris, ETCCNT301 capstone, Part B)
Student : Harshit | Roll no: 2501730196 | K = 96
Extra feature (K mod 3 = 0): write every label and variable with its
address into symbols.txt.

Usage:  python assembler.py Prog.asm        -> Prog.hack + symbols.txt
"""
import sys
import os

# ---------- lookup tables ----------
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        t["R%d" % i] = i
    return t


def clean(line):
    """Remove comments and all whitespace."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def first_pass(lines, symbols):
    """Read 1: drop comments/blank lines and record label addresses."""
    code, rom = [], 0
    for text in lines:
        line = clean(text)
        if not line:
            continue
        if line.startswith("("):               # label  (LOOP)
            symbols[line[1:-1]] = rom          # address of NEXT instruction
        else:
            code.append(line)
            rom += 1
    return code


def encode_c(line):
    dest, jump = "", ""
    if "=" in line:
        dest, line = line.split("=", 1)
    if ";" in line:
        line, jump = line.split(";", 1)
    return "111" + COMP[line] + DEST[dest] + JUMP[jump]


def second_pass(code, symbols):
    """Read 2: turn every line into 16 bits; new variables start at 16."""
    out, next_var = [], 16
    for line in code:
        if line.startswith("@"):
            sym = line[1:]
            if sym.isdigit():
                value = int(sym)
            else:
                if sym not in symbols:         # a new variable
                    symbols[sym] = next_var
                    next_var += 1
                value = symbols[sym]
            out.append(format(value, "016b"))
        else:
            out.append(encode_c(line))
    return out


def write_symbols(symbols, path):
    """Extra feature (K mod 3 = 0): save labels/variables + addresses."""
    builtin = set(predefined())
    with open(path, "w") as f:
        f.write("Symbol table (user labels and variables)\n")
        f.write("%-20s %s\n" % ("Symbol", "Address"))
        for name, addr in sorted(symbols.items(), key=lambda kv: kv[1]):
            if name not in builtin:
                f.write("%-20s %d\n" % (name, addr))


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python assembler.py Prog.asm")
    src = sys.argv[1]
    with open(src) as f:
        lines = f.read().splitlines()
    symbols = predefined()
    code = first_pass(lines, symbols)
    binary = second_pass(code, symbols)
    base = os.path.splitext(src)[0]
    with open(base + ".hack", "w") as f:
        f.write("\n".join(binary) + "\n")
    write_symbols(symbols, os.path.join(os.path.dirname(src) or ".", "symbols.txt"))
    print("Wrote %s.hack (%d instructions) and symbols.txt" % (base, len(binary)))


if __name__ == "__main__":
    main()
