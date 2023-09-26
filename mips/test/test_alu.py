from amaranth.sim import Simulator, Delay, Settle
from mips.cpu.alu import ALU
from mips.cpu.isa import Funct

import pytest

MAX_32U = 0xff_ff_ff_ff

@pytest.mark.parametrize(
        "rs,rt,rd,ovf",
        [
            (1, 2, 3, 0),
            (2, 2, 4, 0),
            (4, 5, 9, 0),
            (8, 8, 16, 0),
            (MAX_32U, 1, 0, 1),
            (1, -1, 0, 0),
        ]
)
def test_add(rs: int, rt: int, rd: int, ovf: bool):
    alu = ALU()
    sim = Simulator(alu)

    def bench():
        yield alu.func.eq(Funct.ADD)
        yield alu.rs.eq(rs)
        yield alu.rt.eq(rt)
        yield Settle()

        res_rd = yield alu.rd
        res_ovf = yield alu.ovf

        assert ovf == res_ovf, f"Expected {Funct.ADD} {rs: 09x} {rt: 09x} to ovf={ovf} but got {res_ovf} instead"
        assert rd == res_rd, f"Expected {Funct.ADD} {rs: 09x} {rt: 09x} for rd=={rd: 09x} but got {res_rd: 09x} instead"
    
        yield Delay(1e-6)
    
    sim.add_process(bench)
    sim.run()
