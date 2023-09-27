from amaranth.sim import Simulator, Delay, Settle
from mips.cpu.alu import ALU
from mips.cpu.isa import Funct

import pytest

from typing import *

MAX_32U = 0xff_ff_ff_ff
MAX_UNSIGN = 0x80_00_00_00
MAX_SIGNED = 0x7f_ff_ff_ff

@pytest.mark.parametrize(
        "rs,rt,rd,ovf",
        [
            (1, 2, 3, 0),
            (2, 2, 4, 0),
            (4, 5, 9, 0),
            (8, 8, 16, 0),
            (MAX_32U, 1, 0, 0),
            (MAX_SIGNED, 1, None, 1),
            (0, -1, 0xffffffff, 0),
            (1, -1, 0, 0),
            (2, -1, 1, 0),
        ]
)
def test_add(rs: int, rt: int, rd: Optional[int], ovf: bool):
    alu = ALU()
    sim = Simulator(alu)

    def bench():
        yield alu.func.eq(Funct.ADD)
        yield alu.rs.eq(rs)
        yield alu.rt.eq(rt)
        yield Settle()

        res_rd = yield alu.rd
        res_ovf = yield alu.ovf

        assert ovf == res_ovf,\
            f"Expected {Funct.ADD} rs:{rs: 09x} rt:{rt: 09x} => rd:{res_rd: 09x} for ovf == {ovf} but got {res_ovf} instead"
        if not ovf:
            assert rd is not None, "rd must not be None if testing for not overflow"
            assert rd == res_rd,\
                f"Expected {Funct.ADD} rs:{rs: 09x} rt:{rt: 09x} => rd:{rd: 09x} but got {res_rd: 09x} instead"
    
        yield Delay(1e-6)
    
    sim.add_process(bench)
    sim.run()

@pytest.mark.parametrize(
        "rs,rt,rd,ovf",
        [
            (1, 1, 0, False),
            (5, 4, 1, False),
            (2, 3, 0xffffffff, False),
            (0, 1, 0xffffffff, False),
            (MAX_UNSIGN, 1, None, True),
        ]
)
def test_sub(rs: int, rt: int, rd: Optional[int], ovf: int):
    alu = ALU()
    sim = Simulator(alu)

    def bench():
        yield alu.func.eq(Funct.SUB)
        yield alu.rs.eq(rs)
        yield alu.rt.eq(rt)
        yield Settle()

        res_rd = yield alu.rd
        res_ovf = yield alu.ovf

        assert ovf == res_ovf,\
            f"Expected {Funct.SUB} rs:{rs: 09x} rt:{rt: 09x} => rd:{res_rd: 09x} for ovf == {ovf} but got {res_ovf} instead"
        if not ovf:
            assert rd is not None, "rd must not be None if testing for not overflow"
            assert rd == res_rd,\
                f"Expected {Funct.SUB} rs:{rs: 09x} rt:{rt: 09x} => rd:{rd: 09x} but got {res_rd: 09x} instead"
    
        yield Delay(1e-6)
    
    sim.add_process(bench)
    sim.run()