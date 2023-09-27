from amaranth import *
from amaranth.sim import Simulator, Settle, Delay

from mips.cpu.isa import Funct

import random

class ALU(Elaboratable):
    """
    Arithmetic Logic Unit

    The design of this unit is currently outputs *both* if the operation
    would trap and the result. It's expected that the consumer of the ALU
    module should perform logic on the output of ``ovf`` before routing.

    It's possible that immediate operations (like ``adi``) can be routed in
    via performing the logic to push them into the register,
    and then reading the result. Same for SLL vs SLLV, where one parses
    a total amount from the instruction and the other from the lower bits
    of a register.
    
    Attributes:
        rs (Signal[32]):    input signal 1
        rt (Signal[32]):    input signal 2
        func (Signal[6]):   input signal specifying function
        rd (Signal[32]):    output signal
        ovf (Signal): overflow signal (used for signalling traps)
    
    """
    def __init__(self):
        # input
        self.rs = Signal(32)
        self.rt = Signal(32)
        self.func = Signal(6)
        # output
        self.rd = Signal(32)
        self.ovf = Signal()

    def elaborate(self, platform):
        m = Module()
        reg = Signal(33)

        with m.Switch(self.func):
            with m.Case(Funct.ADD):
                m.d.comb += [
                    reg.eq(self.rs + self.rt),
                    self.rd.eq(reg)
                ]
                with m.If(self.rs[-1] == self.rt[-1]):
                   m.d.comb += self.ovf.eq(reg[-2] != self.rs[-1])

            with m.Case(Funct.ADDU):
                m.d.comb += [
                    reg.eq(self.rs + self.rt), 
                    self.rd.eq(reg),
                    self.ovf.eq(0)
                ]
            with m.Case(Funct.SUB):
                m.d.comb += [
                    reg.eq(self.rs - self.rt),
                    self.rd.eq(reg)
                ]
                with m.If(self.rs[-1] != self.rt[-1]):
                    m.d.comb += self.ovf.eq(reg[-2] != self.rs[-1])

            with m.Case(Funct.SUBU):
                m.d.comb += [
                    reg.eq(self.rs - self.rt),
                    self.rd.eq(reg),
                ]
            # Logical combinators
            with m.Case(Funct.AND):
                m.d.comb += self.rd.eq(self.rs & self.rt)
            with m.Case(Funct.OR):
                m.d.comb += self.rd.eq(self.rs | self.rt)
            with m.Case(Funct.XOR):
                m.d.comb += self.rd.eq(self.rs ^ self.rt)
            with m.Case(Funct.NOR):
                m.d.comb += self.rd.eq( ~ (self.rs | self.rt) )
            # Shifts
            with m.Case(Funct.SLL):
                m.d.comb += self.rd.eq(self.rs << self.rt[:6])
            with m.Case(Funct.SRA):
                m.d.comb += self.rd.eq(self.rs >> self.rt[:6])
            with m.Case(Funct.SRL):
                m.d.comb += self.rd.eq(self.rs.as_signed() >> self.rt[:6])
            with m.Default():
                pass

        return m


def simulate(file: str):
    alu = ALU()
    MAX_32U = 0xff_ff_ff_ff
    sim = Simulator(alu)

    def bench():
        test_cases = [
            # (funct, rs, rt, rd, ovf)
            (Funct.ADD, 1, 2, 3, 0),
            (Funct.ADD, 2, 2, 4, 0),
            (Funct.ADD, 4, 5, 9, 0),
            (Funct.ADD, 8, 8, 16, 0),
            (Funct.ADD, MAX_32U, 1, 0, 1),
            (Funct.ADD, 1, -1, 0, 0),

            (Funct.ADD, MAX_32U -1, 1, MAX_32U, 0),
            (Funct.ADDU, MAX_32U, 1, 0, 0),

            (Funct.SUB, 4, 1, 3, 0),
            (Funct.SUB, 0, 1, MAX_32U, 1),
            (Funct.SUBU, 0, 1, MAX_32U, 0),

            (Funct.AND, 0b11, 0b00, 0b00, 0),
            (Funct.AND, 0b10, 0b11, 0b10, 0),
            (Funct.AND, 0b11, 0b11, 0b11, 0),
            (Funct.AND, 0b00, 0b00, 0b00, 0),

            (Funct.OR, 0b11, 0b00, 0b11, 0),
            (Funct.OR, 0b10, 0b01, 0b11, 0),
            (Funct.OR, 0b01, 0b01, 0b01, 0),
            (Funct.OR, 0b00, 0b00, 0b00, 0),

            (Funct.XOR, 0b00, 0b00, 0b00, 0),
            (Funct.XOR, 0b10, 0b00, 0b10, 0),
            (Funct.XOR, 0b11, 0b00, 0b11, 0),
            (Funct.XOR, 0b11, 0b01, 0b10, 0),
            (Funct.XOR, 0b11, 0b10, 0b01, 0),

        ]
        for fun, x, y, res, should_trap in test_cases:
                print(f"{fun}\t{x: 09x}\t{y: 09x}\t{res: 09x}\t{'(traps)' if should_trap else ''}", end='')

                yield alu.func.eq(fun)
                yield alu.rs.eq(x)
                yield alu.rt.eq(y)
                yield Settle()

                rt = yield alu.rs
                rs = yield alu.rt
                rd = yield alu.rd
                trap = yield alu.ovf
                try:
                    if should_trap:
                        assert trap == 1,\
                            f"Trap {trap} should have triggered didn't on rt:{rs: 09x}({x: 09x}) + rd:{rt: 09x}({y: 09x}) = rd:{rd: 08x}"
                    else:
                        assert rd == res,\
                            f"{fun} rt:{rs: 09x} rd:{rt: 09x} should be {res: 09x} but was instead {rd: 09x}"
                except AssertionError as e:
                    print(f"\tFAIL:\n\t\t{e}\n")
                else:
                    print("\tPASS")                
                yield Delay(1e-6)

    #sim.add_clock(1e-6) # Is this write for ICE?
    sim.add_process(bench)
    

    with sim.write_vcd(file):
        sim.run()
