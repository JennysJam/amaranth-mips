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
