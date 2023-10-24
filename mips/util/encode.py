"""
Utility functions to encode commands into values
"""

from amaranth import *
from mips.cpu.isa import *
from typing import *

from collections import namedtuple

OPCODE_OFF = 26

FUNCT_OFF = 0

SHAMT_OFF = 6

RD_OFF = SHAMT_OFF + 5

RT_OFF = RD_OFF + 5

RS_OFF = RT_OFF + 5

IMM_OFFSET = 0

ADDR_OFFSET = 0

class Res(NamedTuple):
    inst: int
    opcode: Opcode
    rs: int
    rt: int
    rd: int
    shamt: int
    funct: Funct
    imm: int
    addr: int

def _register(funct: Funct):
    """
    Utility function to generate functions that encode Register Encoded functions

    Arguments:
        funct (Funct):  Funct value
    """
    def func(rs: int, rd: int, rt: int):
            assert 0 <= rs < 32
            assert 0 <= rt <= 32
            assert 0 <= rd <= 32
            # TODO: assert bounds coherently on shamt?

            code: int = (
                Opcode.SPECIAL.value << OPCODE_OFF
                | rs << RS_OFF
                | rt << RT_OFF
                | rd << RD_OFF
                | 0 << SHAMT_OFF
                | funct.value
            )
            parts = (
                code,           # encoding
                Opcode.SPECIAL, # opcode
                rs,             # rs
                rt,             # rt
                rd,             # rd
                0,          # shamt
                funct,          # funct
                0,      # imm,
                0,      # addr
            )
            return parts

    return func

def _shift(funct: Funct):
    """
    Utility function to generate functions that encode Register Encoded functions

    Arguments:
        funct (Funct):  Funct value
    """
    def func(rs: int, rt: int, shamt: int):
            assert 0 <= rs < 32
            assert 0 <= rt <= 32
            # TODO: assert bounds coherently on shamt?

            code: int = (
                Opcode.SPECIAL.value << OPCODE_OFF
                | rs << RS_OFF
                | rt << RT_OFF
                | 0 << RD_OFF
                | shamt << SHAMT_OFF
                | funct.value
            )
            parts = (
                code,           # encoding
                Opcode.SPECIAL, # opcode
                rs,             # rs
                rt,             # rt
                0,             # rd
                shamt,          # shamt
                funct,          # funct
                0,      # imm,
                0,      # addr
            )
            return parts

    return func

def _immediate(opcode: Opcode):
    def func(rs: int, rt: int, imm: int):
        assert opcode in IMM_OPCODE
        assert 0 <= rs < 32
        assert 0 <= rt <= 32
        code: int = (
            opcode.value << OPCODE_OFF
            | rs << RS_OFF
            | rt << RT_OFF
            | imm << IMM_OFFSET
        )

        parts = (
            code,           # encoding
            opcode,         # opcode
            rs,             # rs
            rt,             # rt
            0,             # rd
            0,          # shamt
            0,          # funct
            imm,      # imm,
            0,      # addr
        )
        return parts
    return func


def _jump(op: Opcode):
    def func(addr: int):
        assert op in JMP_OPCODE
        code = (op.value << OPCODE_OFF) | addr 
        parts = (
            code,           # encoding
            op, # opcode
            0,             # rs
            0,             # rt
            0,             # rd
            0,          # shamt
            0,          # funct
            0,      # imm,
            addr,      # addr
        )
        return parts
    return func

ADD = _register(Funct.ADD)

ADDI = _immediate(Opcode.ADDI)

ADDU = _register(Funct.ADDU)

ADDIU = _immediate(Opcode.ADDIU)

SUB = _register(Funct.SUB)

SUBU = _register(Funct.SUBU)

SLL = _shift(Funct.SLL)

SLLV = _register(Funct.SLLV)

SRA = _shift(Funct.SRA)

SRAV = _register(Funct.SRAV)

SRL = _shift(Funct.SRL)

SRLV = _register(Funct.SRLV)

AND = _register(Funct.AND)

ANDI = _immediate(Opcode.ANDI)

NOR = _register(Funct.NOR)

OR = _register(Funct.OR)

ORI = _immediate(Opcode.ORI)

XOR = _register(Funct.XOR)

XORI = _immediate(Opcode.XORI)

SLT = _register(Funct.SLT)

SLTI = _immediate(Opcode.SLTI)

SLTU = _register(Funct.SLTU)

SLTIU = _immediate(Opcode.SLTIU)

J = _jump(Opcode.J)

JAL = _jump(Opcode.JAL)

JALR = _register(Funct.JALR)

JR = _register(Funct.JR)

BEQ = _immediate(Opcode.BEQ)

BNE = _immediate(Opcode.BNE)

BLEZ = _immediate(Opcode.BLEZ)

BGTZ = _immediate(Opcode.BGTZ)

LLO = _immediate(Opcode.LLO)

LHI = _immediate(Opcode.LHI)

# TODO: TRAP

LB = _immediate(Opcode.LB)

LW = _immediate(Opcode.LW)

LBU = _immediate(Opcode.LBU)

LH = _immediate(Opcode.LHU)

LHU = _immediate(Opcode.LHU)

SB = _immediate(Opcode.SB)

SH = _immediate(Opcode.SH)

SW = _immediate(Opcode.SW)

MFHI = _register(Funct.MFHI)

MFLO = _register(Funct.MFLO)

MTHI = _register(Funct.MTHI)

MTLO = _register(Funct.MTLO)