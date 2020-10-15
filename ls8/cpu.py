"""CPU functionality."""

import sys

ADD = 0b10100000
HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.ram = [0] * 256
        self.sp = 255
    #     self.branchtable = {}
    #     self.branchtable[ADD] = self.handle_ADD
    #     self.branchtable[HLT] = self.handle_HLT
    #     self.branchtable[LDI] = self.handle_LDI
    #     self.branchtable[MUL] = self.handle_MUL
    #     self.branchtable[PRN] = self.handle_PRN

    # def handle_ADD(self, operand1, operand2):
    #     self.alu('ADD', operand1, operand2)
    #     self.pc += 3

    # def handle_HLT(self, operand1, operand2):
    #     sys.exit(0)

    # def handle_LDI(self, operand1, operand2):
    #     self.reg[operand1] = operand2
    #     self.pc += 3

    # def handle_MUL(self, operand1, operand2):
    #     self.alu('MUL', operand1, operand2)
    #     self.pc += 3

    # def handle_PRN(self, operand1, operand2):
    #     print(self.reg[operand1]) 
    #     self.pc += 2

    def ram_read(self, mar):
        self.mdr = self.ram[mar]
        return self.ram[mar]
    # memory data register- mdr(data)
    # memory address register- mar(address)

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, input_program=[]):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
        # Address and pc both are similar in that they both refer to an index inside the memory array.
        # But address is just temporarily used when loading memory before running the CPU.
        # pc is used to keep track of the currently-executing instruction while running the CPU.
        address = 0
        if len(input_program) > 0:
            program = input_program
        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # lambda expression - lambda op1, op2: self.alu('ADD', op1, op2)
        # elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # def run(self):
    #     """Run the CPU."""
    #     halted = False
    #     while not halted:
    #         self.trace()
    #         self.ir = self.ram_read(self.pc)

    #         operand1 = self.ram_read(self.pc + 1)
    #         operand2 = self.ram_read(self.pc + 2)

    #         self.branchtable[self.ir](operand1, operand2)

            # num_operands = self.ir >> 6
            # operand1 = None
            # operand2 = None
            # if num_operands == 2:
            #     operand1 = self.ram_read(self.pc + 1)
            #     operand2 = self.ram_read(self.pc + 2)
            # elif num_operands == 1:
            #     operand1 = self.ram_read(self.pc + 1)
            #
            # self.branchtable[self.ir](operand1, operand2)

    def run(self):
        """Run the CPU."""
        halted = False
        while not halted:
            self.trace()
            self.ir = self.ram_read(self.pc)
            if self.ir == ADD:
                operand1 = self.ram_read(self.pc + 1)
                operand2 = self.ram_read(self.pc + 2)
                self.alu('ADD', operand1, operand2)
                self.pc += 3
            elif self.ir == HLT:
                halted = True
            elif self.ir == LDI:
                operand1 = self.ram_read(self.pc + 1)
                operand2 = self.ram_read(self.pc + 2)
                self.reg[operand1] = operand2
                self.pc += 3
            elif self.ir == MUL:
                operand1 = self.ram_read(self.pc + 1)
                operand2 = self.ram_read(self.pc + 2)
                self.alu('MUL', operand1, operand2)
                self.pc += 3
            elif self.ir == PRN:
                operand1 = self.ram_read(self.pc + 1)
                print(self.reg[operand1])
                self.pc += 2

    # def run(self):
    #     """Run the CPU."""
    #     running = True
    #     while running is True:
    #         ir = self.ram[self.pc]
    #         operand_a = self.ram_read(self.pc + 1)
    #         operand_b = self.ram_read(self.pc + 2)
    #         if ir == HLT:
    #             #HLT
    #             running = False
    #         elif ir == LDI:
    #             #LDI
    #             reg_num = operand_a
    #             value = operand_b
    #             self.register[reg_num] = value
    #             self.pc += 3
    #         elif ir == PRN:
    #             #PRN
    #             reg_num = operand_a
    #             print(self.register[reg_num])
    #             self.pc += 2
    #         else:
    #             print("Unknown instruction")
    #             sys.exit(0)

            elif self.ir == PUSH:
                # Decrement the stack pointer
                self.sp -= 1
                # Grab the value out of the given register
                reg_num = self.ram_read(self.pc + 1)
                value = self.reg[reg_num]  # this is what we want to push

                # Copy the value onto the stack
                top_of_stack = self.sp
                self.ram[top_of_stack] = value
                self.pc += 2
                # print(self.ram[0xf0:0xf4])

            elif self.ir == POP:
                # Get value from top of stack
                top_of_stack = self.sp
                value = self.ram[top_of_stack]
                reg_num = self.ram_read(self.pc + 1)
                self.reg[reg_num] = value
                # Increment the SP
                self.sp += 1
                self.pc += 2
            else:
                print(f'unknown instruction {self.ir} at address {self.pc}')
                sys.exit(1)

