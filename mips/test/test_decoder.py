from amaranth.sim import Simulator, Delay, Settle
from mips.cpu.decoder import Decoder
from mips.cpu.isa import *
import mips.util.encode as encode
import pytest

from typing import *

@pytest.mark.parametrize(
        "inst, op, rs, rt, rd, shamt, funct, imm, addr",
        [
            (0x00221820, Opcode.SPECIAL, 1, 2, 3, 0, Funct.ADD, 0, 0),
            (0x08000000, Opcode.J,       0, 0, 0, 0, 0,         0, 0),
            encode.ADD(rs=1, rt=1, rd=1),
            encode.ADD(rs=1, rt=1, rd=2),
            encode.ADD(rs=1, rt=2, rd=3),
            
            encode.ADDI(rs=1, rt=2, imm=24),

            encode.ADDU(rs=3, rt=2, rd=1),

            encode.ADDU(rs=31, rt=31, rd=31),

            encode.ADDIU(rs=3, rt=2, imm=26),

            encode.AND(rs=3, rt=4, rd=5),

            encode.ANDI(rs=3, rt=4, imm=26),

            encode.NOR(rs=9, rt=8, rd=7),

            encode.OR(rs=4, rt=6, rd=10),

            encode.ORI(rs=1, rt=3, imm=31),

            encode.SLLV(rs=1, rt=2, rd=3),

            encode.SLL(rs=2, rt=1, shamt=0),

            encode.SRA(rs=1, rt=2, shamt=0),

            encode.SRAV(rs=1, rt=2, rd=3),

            encode.SRL(rs=1, rt=2, shamt=0),

            encode.SRLV(rs=1, rt=2, rd=0),

            encode.XOR(rs=3, rt=4, rd=9),

            encode.XORI(rs=5, rt=9, imm=2006),

            encode.LHI(rs=3, rt=4, imm=256),

            encode.LLO(rs=4, rt=17, imm=10),

            encode.SLT(rs=31, rt=30, rd=29),

            encode.SLTU(rs=20, rt=30, rd=29),

            encode.SLTI(rs=20, rt=10, imm=1999),

            encode.SLTIU(rs=22, rt=10, imm=30),         

            encode.BEQ(rs=1, rt=2 , imm=400),

            encode.BGTZ(rs=2, rt=3, imm=500),

            encode.BLEZ(rs=10, rt=4, imm=200),

            encode.BNE(rs=9, rt=8, imm=7),

            encode.J(2000),

            encode.JAL(1000),

            encode.JALR(rs=30, rt=0, rd=10),

            encode.JR(rs=10, rt=0, rd=20),

            encode.LB(rs=1, rt=2, imm=40),

            encode.LBU(rs=1, rt=2, imm=33),

            encode.LH(rs=1, rt=10, imm=200),

            encode.LHU(rs=10, rt=15, imm=30),

            encode.LW(rs=8, rt=16, imm=30),

            encode.SB(rs=10, rt=20, imm=300),

            encode.SH(rs=22, rt=1, imm=400),

            encode.MFHI(rs=0, rt=0, rd=20),

            encode.MFLO(rs=0, rt=0, rd=2),

            encode.MTLO(rs=0, rt=0, rd=16),

            encode.MTHI(rs=0, rt=0, rd=8)
        ]
)
def test_adhoc_coverage(
    inst: Instr,
    op: Opcode,
    rs: int,
    rt: int,
    rd: int,
    shamt: int,
    funct: Funct,
    imm: int,
    addr: int):
    """
    Adhoc coverage of all of the functions
    """
    
    if isinstance(funct, Funct):
        funct = funct.value

    decoder = Decoder()
    sim = Simulator(decoder)
    
    def test():
        yield decoder.inst.eq(inst)
        yield Settle()

        
        my_op = yield decoder.opcode
        my_rs = yield decoder.rs
        my_rt = yield decoder.rt
        my_rd = yield decoder.rd
        my_func = yield decoder.funct
        my_shamt = yield decoder.shamt
        my_imm = yield decoder.imm
        my_addr = yield decoder.addr
        
        print(f"inst={inst:032b}")
        print(f"my_op{my_op:05b}")
        print(f"my_rs={my_rs:05b}")
        print(f"my_rt={my_rt:05b}")
        print(f"my_rd={my_rd:05b}")
        print(f"my_shamt={my_shamt:05b}")
        print(f"my_func{my_func:06b}")
        print(f"my_imm={my_imm:016b}")
        print(f"my_addr={my_addr:026b}")

        assert my_op == op.value
        assert my_rt == rt
        assert my_rs == rs
        assert my_rd == rd
        assert my_func == funct
        assert my_shamt == shamt
        assert my_imm == imm
        assert my_addr == addr

        yield Delay(1e-6)
    
    sim.add_process(test)
    sim.run()