- [ ] build an ALU module that takes in an rs and rt value, adds them, and produces an rd
- [ ] extend the ALU to also take a funct value and use it to determine what operation to do
- [ ] build a decoder module that takes in a 32-bit value and spits out the fields of the instruction
    + [ ] instruction in; opcode, rs, rt, rd, shamt, funct, imm, addr out
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

:sparkles: you now have basically a cpu (it can't branch but it can calculate!)