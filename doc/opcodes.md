# MIPS Encoding Reference

-----

## Instruction Encodings

Each MIPS instruction is encoded in exactly one word (32 bits). There
are three encoding formats.

### Register Encoding

This encoding is used for instructions which do not require any
immediate data. These instructions receive all their operands in
registers. Additionally, certain of the bit shift instructions use this
encoding; their operands are two registers and a 5-bit shift amount.

    ooooooss sssttttt dddddhhh hhffffff

| Field | Width | Description                                                                                                                             |
| ----- | ----- | --------------------------------------------------------------------------------------------------------------------------------------- |
| o     | 6     | Instruction opcode. This is 000_000 for instructions using this encoding.                                                               |
| s     | 5     | First source register, in the range 0-31.                                                                                               |
| t     | 5     | Second source register, in the range 0-31.                                                                                              |
| d     | 5     | Destination register, in the range 0-31.                                                                                                |
| h     | 5     | Shift amount, for shift instructions.                                                                                                   |
| f     | 6     | Function. Determines which operation is to be performed. Values for this field are documented in the tables at the bottom of this page. |

### Immediate Encoding

This encoding is used for instructions which require a 16-bit immediate
operand. These instructions typically receive one operand in a register,
another as an immediate value coded into the instruction itself, and
place their results in a register. This encoding is also used for load,
store, branch, and other instructions so the use of the fields is
different in some cases.

Note that the "first" and "second" registers are not always in this
order in the assembly language; see "Instruction Syntax" for details.

    ooooooss sssttttt iiiiiiii iiiiiiii

| Field | Width | Description                                                                                                                                                                                                 |
| ----- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| o     | 6     | Instruction opcode. Determines which operation is to be performed. Values for this field are documented in the tables at the bottom of this page.                                                           |
| s     | 5     | First register, in the range 0-31.                                                                                                                                                                          |
| t     | 5     | Second register, in the range 0-31.                                                                                                                                                                         |
| i     | 16    | Immediate data. These 16 bits of immediate data are interpreted differently for different instructions. 2's-complement encoding is used to represent a number between -2<sup>15</sup> and 2<sup>15</sup>-1. |

### Jump Encoding

This encoding is used for jump instructions, which require a 26-bit
immediate offset. It is also used for the trap instruction.

    ooooooaa aaaaaaaa aaaaaaaa aaaaaaaa

| Field | Width | Description                                                                                                                                                                                                 |
| ----- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| o     | 6     | Instruction opcode. Determines which operation is to be performed. Values for this field are documented in the tables at the bottom of this page.                                                           |
| a     | 26    | Immediate data. These 26 bits of immediate data are interpreted differently for different instructions. 2's-complement encoding is used to represent a number between -2<sup>25</sup> and 2<sup>25</sup>-1. |

## Instruction Syntax

This is a table of all the different types of instruction as they appear
in the assembly listing. Note that each syntax is associated with
exactly one encoding which is used to encode all instructions which use
that syntax.

| Encoding  | Syntax    | Template          | Comments                                            |
| --------- | --------- | ----------------- | --------------------------------------------------- |
| Register  | ArithLog  | `f $d, $s, $t`    |                                                     |
|           | DivMult   | `f $s, $t`        |                                                     |
|           | Shift     | `f $d, $t, h`     |                                                     |
|           | ShiftV    | `f $d, $t, $s`    |                                                     |
|           | JumpR     | `f $s`            |                                                     |
|           | MoveFrom  | `f $d`            |                                                     |
|           | MoveTo    | `f $s`            |                                                     |
| Immediate | ArithLogI | `o $t, $s, i`     |                                                     |
|           | LoadI     | `o $t, immed32`   | i is high or low 16 bits of immed32                 |
|           | Branch    | `o $s, $t, label` | i is calculated as `(label - (current + 4)) \>\> 2` |
|           | BranchZ   | `o $s, label`     | i is calculated as `(label - (current + 4)) \>\> 2` |
|           | LoadStore | `o $t, i ($s)`    |                                                     |
| Jump      | Jump      | `o label`         | i is calculated as `(label - (current + 4)) \>\> 2` |
|           | Trap      | `o a`             |

## Opcode Table

These tables list all of the available operations in MIPS. For each
instruction, the 6-bit opcode or function is shown. The syntax column
indicates which syntax is used to write the instruction in assembly text
files. Note that which syntax is used for an instruction also determines
which encoding is to be used. Finally the operation column describes
what the operation does in pseudo-Java plus some special notation as
follows:

`MEM [a]:n` means the *n* bytes of memory starting with address *a*.  
The address must always be aligned; that is, *a* must be divisible by
*n*, which must be a power of 2.

`LB (x)` means the least significant 8 bits of the 32-bit location
*x*.  
`LH (x)` means the least significant 16 bits of the 32-bit location
*x*.  
`HH (x)` means the most significant 16 bits of the 32-bit location
*x*.

"`SE (x)`" means the 32-bit quantity obtained by extending the value *x*
on the left with its most significant bit.  
"`ZE (x)`" means the 32-bit quantity obtained by extending the value *x*
on the left with 0 bits.

### Arithmetic and Logical Instructions

| Instruction | Type      | Opcode/Function | Syntax    | Operation                  |
| ----------- | --------- | --------------- | --------- | -------------------------- |
| **add**     | Register  | 100_000         | ArithLog  | $d = $s + $t               |
| **addu**    | Register  | 100_001         | ArithLog  | $d = $s + $t               |
| **addi**    | Immediate | 001_000         | ArithLogI | $t = $s + SE(i)            |
| **addiu**   | Immediate | 001_001         | ArithLogI | $t = $s + SE(i)            |
| **and**     | Register  | 100_100         | ArithLog  | $d = $s & $t               |
| **andi**    | Immediate | 001_100         | ArithLogI | $t = $s & ZE(i)            |
| **div**     | Register  | 011_010         | DivMult   | lo = $s / $t; hi = $s % $t |
| **divu**    | Register  | 011_011         | DivMult   | lo = $s / $t; hi = $s % $t |
| **mult**    | Register  | 011_000         | DivMult   | hi:lo = $s \* $t           |
| **multu**   | Register  | 011_001         | DivMult   | hi:lo = $s \* $t           |
| **nor**     | Register  | 100_111         | ArithLog  | $d = \~($s \| $t)          |
| **or**      | Register  | 100_101         | ArithLog  | $d = $s \| $t              |
| **ori**     | Immediate | 001_101         | ArithLogI | $t = $s \| ZE(i)           |
| **sll**     | Register  | 000_000         | Shift     | $d = $t \<\< h             |
| **sllv**    | Register  | 000_100         | ShiftV    | $d = $t \<\< $s            |
| **sra**     | Register  | 000_011         | Shift     | $d = $t \>\> h             |
| **srav**    | Register  | 000_111         | ShiftV    | $d = $t \>\> $s            |
| **srl**     | Register  | 000_010         | Shift     | $d = $t \>\>\> h           |
| **srlv**    | Register  | 000_110         | ShiftV    | $d = $t \>\>\> $s          |
| **sub**     | Register  | 100_010         | ArithLog  | $d = $s - $t               |
| **subu**    | Register  | 100_011         | ArithLog  | $d = $s - $t               |
| **xor**     | Register  | 100_110         | ArithLog  | $d = $s ^ $t               |
| **xori**    | Immediate | 001_110         | ArithLogI | $d = $s ^ ZE(i)            |

### Constant-Manipulating Instructions

| Instruction | Type      | Opcode/Function | Syntax | Operation     |
| ----------- | --------- | --------------- | ------ | ------------- |
| **lhi**     | Immediate | 011_001         | LoadI  | `HH ($t) = i` |
| **llo**     | Immediate | 011_000         | LoadI  | `LH ($t) = i` |

#### Comparison Instructions

| Instruction | Type      | Opcode/Function | Syntax    | Operation          |
| ----------- | --------- | --------------- | --------- | ------------------ |
| **slt**     | Register  | 101_010         | ArithLog  | $d = ($s \< $t)    |
| **sltu**    | Register  | 101_001         | ArithLog  | $d = ($s \< $t)    |
| **slti**    | Immediate | 001_010         | ArithLogI | $t = ($s \< SE(i)) |
| **sltiu**   | Immediate | 001_001         | ArithLogI | $t = ($s \< SE(i)) |

### Branch Instructions

| Instruction | Type | Opcode/Function | Syntax  | Operation                     |
| ----------- | ---- | --------------- | ------- | ----------------------------- |
| **beq**     | Jump | 000_100         | Branch  | if ($s == $t) pc += i \<\< 2  |
| **bgtz**    | Jump | 000_111         | BranchZ | if ($s \> 0) pc += i \<\< 2   |
| **blez**    | Jump | 000_110         | BranchZ | if ($s \<= 0) pc += i \<\< 2  |
| **bne**     | Jump | 000_101         | Branch  | if ($s \!= $t) pc += i \<\< 2 |

### Jump Instructions

| Instruction | Type | Opcode/Function | Syntax | Operation                |
| ----------- | ---- | --------------- | ------ | ------------------------ |
| **j**       | Jump | 000_010         | Jump   | pc += i \<\< 2           |
| **jal**     | Jump | 000_011         | Jump   | $31 = pc; pc += i \<\< 2 |
| **jalr**    | Jump | 001_001         | JumpR  | $31 = pc; pc = $s        |
| **jr**      | Jump | 001_000         | JumpR  | pc = $s                  |

### Load Instructions

| Instruction | Type      | Opcode/Function | Syntax    | Operation                  |
| ----------- | --------- | --------------- | --------- | -------------------------- |
| **lb**      | Immediate | 100_000         | LoadStore | `$t = SE (MEM [$s + i]:1)` |
| **lbu**     | Immediate | 100_100         | LoadStore | `$t = ZE (MEM [$s + i]:1)` |
| **lh**      | Immediate | 100_001         | LoadStore | `$t = SE (MEM [$s + i]:2)` |
| **lhu**     | Immediate | 100_101         | LoadStore | `$t = ZE (MEM [$s + i]:2)` |
| **lw**      | Immediate | 100_011         | LoadStore | `$t = MEM [$s + i]:4`      |

### Store Instructions

| Instruction | Type      | Opcode/Function | Syntax    | Operation                  |
| ----------- | --------- | --------------- | --------- | -------------------------- |
| **sb**      | Immediate | 101_000         | LoadStore | `MEM [$s + i]:1 = LB ($t)` |
| **sh**      | Immediate | 101_001         | LoadStore | `MEM [$s + i]:2 = LH ($t)` |
| **sw**      | Immediate | 101_011         | LoadStore | `MEM [$s + i]:4 = $t`      |

### Data Movement Instructions

| Instruction | Type      | Opcode/Function | Syntax   | Operation |
| ----------- | --------- | --------------- | -------- | --------- |
| **mfhi**    | Immediate | 010_000         | MoveFrom | $d = hi   |
| **mflo**    | Immediate | 010_010         | MoveFrom | $d = lo   |
| **mthi**    | Immediate | 010_001         | MoveTo   | hi = $s   |
| **mtlo**    | Immediate | 010_011         | MoveTo   | lo = $s   |

### Exception and Interrupt Instructions

| Instruction | Type | Opcode/Function | Syntax | Operation |
| ----------- | ---- | --------------- | ------ | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **trap**    | Trap | 011_010         | ???    | Trap      | Dependent on operating system; different values for immed26 specify different operations. See the [list of traps](traps) for information on what the different trap codes do. |

## Opcode And Funct values

### Opcode (Immediate, Jump and Trap encodings)

Table of opcodes for all instructions (REG indicates SPECIAL0 encoding
which will take a Funct value.)

|     | 000  | 001   | 010  | 011   | 100  | 101 | 110  | 111  |
| --- | ---- | ----- | ---- | ----- | ---- | --- | ---- | ---- |
| 000 | REG  |       | j    | jal   | beq  | bne | blez | bgtz |
| 001 | addi | addiu | slti | sltiu | andi | ori | xori |      |
| 010 |      |       |      |       |      |     |      |      |
| 011 | llo  | lhi   | trap |       |      |     |      |      |
| 100 | lb   | lh    |      | lw    | lbu  | lhu |      |      |
| 101 | sb   | sh    |      | sw    |      |     |      |      |
| 110 |      |       |      |       |      |     |      |      |
| 111 |      |       |      |       |      |     |      |      |

| Opcode    | Encoding |
| --------- | -------- |
| **REG**   | 000_000  |
| **j**     | 000_010  |
| **jal**   | 000_011  |
| **beq**   | 000_100  |
| **bne**   | 000_101  |
| **blez**  | 000_110  |
| **bgtz**  | 000_111  |
| **addi**  | 001_000  |
| **addiu** | 000_001  |
| **slti**  | 001_010  |
| **sltiu** | 001_011  |
| **andi**  | 001_100  |
| **ori**   | 001_101  |
| **xori**  | 001_110  |
| **llo**   | 011_000  |
| **lhi**   | 011_001  |
| **trap**  | 011_010  |
| **lb**    | 100_000  |
| **lh**    | 100_001  |
| **lw**    | 100_011  |
| **lbu**   | 100_100  |
| **lhu**   | 100_101  |
| **sb**    | 101_000  |
| **sh**    | 101_001  |
| **sw**    | 101_011  |


### Funct (Register encoding)

Table of function codes for register-format instructions:

|     | 000  | 001   | 010  | 011  | 100  | 101 | 110  | 111  |
| --- | ---- | ----- | ---- | ---- | ---- | --- | ---- | ---- |
| 000 | sll  |       | srl  | sra  | sllv |     | srlv | srav |
| 001 | jr   | jalr  |      |      |      |     |      |      |
| 010 | mfhi | mthi  | mflo | mtlo |      |     |      |      |
| 011 | mult | multu | div  | divu |      |     |      |      |
| 100 | add  | addu  | sub  | subu | and  | or  | xor  | nor  |
| 101 |      |       | slt  | sltu |      |     |      |      |
| 110 |      |       |      |      |      |     |      |      |
| 111 |      |       |      |      |      |     |      |      |

Reference of Funct -\> Encoding:

| Opcode    | Encoding |
| --------- | -------- |
| **sll**   | 000_000  |
| **srl**   | 000_010  |
| **sra**   | 000_011  |
| **sllv**  | 000_100  |
| **srlv**  | 000_110  |
| **srav**  | 000_111  |
| **jr**    | 001_000  |
| **jalr**  | 001_001  |
| **mfhi**  | 010_000  |
| **mthi**  | 010_001  |
| **mflo**  | 010_010  |
| **mtlo**  | 010_011  |
| **mult**  | 011_000  |
| **multu** | 011_001  |
| **div**   | 011_010  |
| **divu**  | 011_011  |
| **add**   | 100_000  |
| **addu**  | 100_001  |
| **sub**   | 100_010  |
| **subu**  | 100_011  |
| **and**   | 100_100  |
| **or**    | 100_101  |
| **xor**   | 100_110  |
| **nor**   | 100_111  |
| **slt**   | 101_011  |
| **sltu**  | 101_011  |