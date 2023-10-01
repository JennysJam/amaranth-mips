from amaranth import *
from amaranth.lib import enum
from amaranth.lib import data

__all__ = [
    "EnumEncoding",
    "Funct",
    "Opcode",
    "Instr"
]

class EnumEncoding(enum.Enum, shape=2):
    """
    Utility class to describe what sort of encoding
    a value has.
    """
    Register = 0
    Immediate = 1
    Jump = 2

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
    SPECIAL = 0
    "Special encoding for instructions that take register"
    J = 0b000_010
    JAL = 0b000_011
    BEQ = 0b000_100
    BNE = 0b000_101
    BLEZ = 0b000_110
    BGTZ = 0b000_111
    ADDI = 0b001_000
    ADDIU = 0b001_001
    SLTI = 0b001_010
    SLTIU = 0b001_011
    ANDI = 0b001_100
    ORI = 0b001_101
    XORI = 0b001_110
    LLO = 0b011_000
    LHI = 0b011_001
    TRAP = 0b011_010
    LB = 0b100_001
    LW = 0b100_011
    LBU = 0b100_100
    LHU = 0b100_101
    SB = 0b101_000
    SH = 0b101_001
    SW = 0b101_011




class RegData(data.Struct):
    """
    Representations the non-Opcode values of a 
    register encoded instruction
    
    Attributes:
        rs (unsigned(5)): First source register
        rt (unsigned(5)): Second source register
        rd (unsigned(5)): Destination register
        h (unsigned(5)): Fixed sized shift amount
        funct (Funct): Function value
    """
    rs: 5
    rt: 5
    rd: 5
    h: 5
    funct: Funct

class ImmData(data.Struct):
    """
    Implements not-Opcode parts of Immediate encoded
    register value

    Attributes:
        rs: First register
        rt: Second register
        imm: Constant immediate value
    """
    rs: 5
    rt: 5
    imm: 16

class JumpData(data.Struct):
    """
    Implements non-Opcode parts of Jump encoded value.

    Attributes:
        addr: Address value
    """
    addr: 26

class Data(data.Union):
    reg: RegData
    imm: ImmData
    jmp: JumpData


class Instr(data.Struct):
    """
    Representation of an instruction as a 
    discriminated union.
    """
    opcode: Opcode
    data: Data
