"""CPU functionality."""

# import sys

ADD = 0b10100000
HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111

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

    def ram_read(self, mar):
        self.mdr = self.ram[mar]
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, input_program=[]):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
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



