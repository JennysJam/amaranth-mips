from amaranth import *
from amaranth.sim import Simulator, Settle, Delay
from mips.cpu.register_file import RegisterFile

def test_register_file_simple():
    reg_file = RegisterFile(
        init=[
            0xffff_ffff
            for _ in range(0,31)
        ]
        )
    sim = Simulator(reg_file)

    def func():
        yield reg_file.rs.eq(1)
        yield reg_file.rt.eq(0)

        yield Settle()

        rs = yield reg_file.rs_out
        rt = yield reg_file.rt_out

        assert rs == 0xffff_ffff
        assert rt == 0
        
        yield Delay(1e-6)
    
    sim.add_process(func)

    sim.run()