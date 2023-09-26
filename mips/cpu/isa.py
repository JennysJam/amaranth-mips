from amaranth.lib import enum

class Funct(enum.Enum, shape=6):
    """
    Binary encoding of instructions with 0b00000 opcode
    """
    ## TODO: Check the binary encoding is right?
    # Add
    ADD = 0b100000
    "trapping add"
    ADDU = 0b100001
    "non-trapping add"
    # div/mul: not implemented

    SLL = 0b000000
    SLLV = 0b000100

    SRA = 0b000011
    SRAV = 0b000111

    SRL = 0b000010
    SRLV = 0b000110

    # AND
    AND = 0b100100
    "And"
    
    NOR = 0b100111
    OR = 0B100101

    SUB = 0b100010
    SUBU = 0b100011

    XOR = 0b100110


