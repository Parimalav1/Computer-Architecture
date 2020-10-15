ls8.py
It is importing everything from CPU, reading the program, passing instructions to CPU and running CPU.

cpu.py
In class CPU object, it got all the variables, defined the functions and ALU operations, a code to run(read addresses from program counter(pc) to instruction register(ir)) the program in a sequence.

examples/print8.ls8
The file has binary digits for load immediate(LDI), register 0(R0), value 8, for printing(PRN) 8 and halt(HLT) the program.

examples/mult.ls8
The file has binary digits for load immediate(LDI), registers (R0, R1), values 8 & 9, ALU operation-MUL(multiply), printing(PRN) the value stored in RO and halt(HLT) the program.

CODE
code in python language to assembly language(# LDI R0,8) by compiler
assembly language(# LDI R0,8) to machine language(binary digits) by assembler