from amaranth import *
from amaranth.lib import enum
from amaranth.lib import data

__all__ = [
    "EnumEncoding",
    "Funct",
    "Opcode",
    "Instr",
    "REG_OPCODE",
    "IMM_OPCODE",
    "JMP_OPCODE"
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
    "Logical/Arithmetic left shift with encoded constant shift value"
    SLLV = 0b000_100
    "Logical/Arithmetic left shift with register shift value"
    SRA = 0b000011
    "Arithmetic right shift with encoded constant shift value"
    SRAV = 0b000_111
    "Arithmetic right shift using register shift value"
    SRL = 0b000010
    "Logical right shift using encoded constant shift value"
    SRLV = 0b000_110
    "Logical shift right using register shift value"
    AND = 0b100100
    "Binary And"
    NOR = 0b100111
    "Binary Nor"
    OR = 0B100101
    "Binary Or"
    SUB = 0b100010
    "Subtract, trap on underflow"
    SUBU = 0b100011
    "Subtract, don't trap"
    XOR = 0b100110
    "Binary xor"
    SLT = 0b101_010
    "Signed less than using register value"
    SLTU = 0b101_001
    "Unsigned less than using register value"
    JALR = 0b001_001
    "Call procedure provided within register"
    JR = 0b001_000
    "Jump to address stored in register"
    MFHI = 0b010_000
    MFLO = 0b010_010
    MTHI = 0b010_001
    MTLO = 0b010_011    

class Opcode(enum.Enum, shape=6):
    SPECIAL = 0
    "Special encoding for instructions that take register"
    J = 0b000_010
    "Jump within current current 256MB region"
    JAL = 0b000_011
    "Call procedure within current 256MB region"
    BEQ = 0b000_100
    BNE = 0b000_101
    BLEZ = 0b000_110
    BGTZ = 0b000_111
    ADDI = 0b001_000
    "Trapping add with sign extended immediate"
    ADDIU = 0b001_001
    "Non-trapping add with sign extended immediate"
    SLTI = 0b001_010
    "Signed less than using immediate"
    SLTIU = 0b001_011
    "Unsigned less than using sign extended immediate"
    ANDI = 0b001_100
    "Bitwise and using zero extended immediate"
    ORI = 0b001_101
    "Bitwise or using zero extended immediate"
    XORI = 0b001_110
    "Bitwise xor using zero extended immediate"
    LLO = 0b011_000
    LHI = 0b011_001
    TRAP = 0b011_010
    LB = 0b100_001
    LW = 0b100_011
    LBU = 0b100_100
    LH = 0b100_001
    LHU = 0b100_101
    SB = 0b101_000
    SH = 0b101_001
    SW = 0b101_011
    

REG_OPCODE = [
    Opcode.SPECIAL
]
"Opcodes that have a register encoding"


IMM_OPCODE = [
    Opcode.ADDI,
    Opcode.ADDIU,
    Opcode.ANDI,
    Opcode.ORI,
    Opcode.XORI,
    Opcode.LHI,
    Opcode.LLO,
    Opcode.SLTI,
    Opcode.SLTIU,
    Opcode.LB,
    Opcode.LBU,
    Opcode.LH,
    Opcode.LHU,
    Opcode.LW,
    Opcode.SB,
    Opcode.SH,
    Opcode.SW,
    Opcode.BEQ,
    Opcode.BNE,
    Opcode.BGTZ,
    Opcode.BLEZ
]
"Opcodes with a immediate style encoding"


JMP_OPCODE = [
    Opcode.J,
    Opcode.JAL,
    Opcode.TRAP
]
"Opcode with a jump-family encoding"

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
    funct: Funct
    shamt: 5
    rd: 5
    rt: 5
    rs: 5
    
    
    
    


class ImmData(data.Struct):
    """
    Implements not-Opcode parts of Immediate encoded
    register value

    Attributes:
        rs: First register
        rt: Second register
        imm: Constant immediate value
    """
    imm: 16
    rt: 5
    rs: 5
    



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
    data: Data
    opcode: Opcode