from amaranth import *
from amaranth.lib import enum
from amaranth.lib import data


class Funct(enum.Enum, shape=6):
    """
    Binary encoding of instructions with 0b00000 opcode
    """
    ADD = 0b100000
    "trapping add"
    ADDU = 0b100001
    "non-trapping add"
    SLL = 0b000000
    SRA = 0b000011
    SRL = 0b000010
    AND = 0b100100
    "And"
    NOR = 0b100111
    OR = 0B100101
    SUB = 0b100010
    SUBU = 0b100011
    XOR = 0b100110

class Opcode(enum.Enum, shape=6):
    pass

class Instr(data.Struct):
    opcode: Opcode
    layout: data.UnionLayout({
        "reg": data.StructLayout({
            "rs": unsigned(5),
            "rt": unsigned(5),
            "rd": unsigned(5),
            "a": unsigned(5),
            "funct": Funct
            }),
        "imm": data.StructLayout({
            "rs": unsigned(5),
            "rt": unsigned(5),
            "imm": unsigned(16)
        }),
        "jmp": data.StructLayout({
            "imm": unsigned(26)
        })
    })