# Amaranth Mips

This implements a simple version of MIPS 2 (the list of handled opcodes is stored in docs) in Amaranth, the Python HDL.

## Usage

Most of the code is handled via testing, which can be evoked with the `./test.sh` script. The `mips` CPU also itself acts as a CLI interface, altho most of the current operations are stubs that throw not implemented errors.

## Progress

- [x] build an ALU module that takes in an rs and rt value, adds them, and produces an rd
- [x] extend the ALU to also take a funct value and use it to determine what operation to do
- [x] build a decoder module that takes in a 32-bit value and spits out the fields of the instruction
    + [x] instruction in; opcode, rs, rt, rd, shamt, funct, imm, addr out
- [ ] build a register file module
    + [ ] takes in an rs, rt, spits out their stored values combinatorially
    + [ ] takes in an write enable, rd, and value, stores the value on the next cycle if enabled
- [ ] wire up the register file and ALU
    + [ ] just use a constant rs, rt, rd and funct
- [ ] wire up the decoder to the RF and ALU
    + [ ] use the same constant instruction from above
- [ ] create a program memory module that takes in an address and spits out a 32-bit instruction combinatorially
    + [ ] the program data just as constants inside the module
- [ ] wire up the program memory module to the decoder, hard-wire the address
- [ ] make a pc register, increment it on every cycle, and hook it up to the address of the program memory
