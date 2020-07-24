"""CPU functionality."""

import sys

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.reg[7] = 0xF4
        self.sp = 7
        self.fl = [0] * 8
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[ADD] = self.handle_add
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[NOP] = self.handle_nop
        self.branchtable[POP] = self.handle_pop
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne
        self.branchtable[JGE] = self.operand_jge
        self.branchtable[JGT] = self.operand_jgt
        self.branchtable[JLE] = self.operand_jle
        self.branchtable[JLT] = self.operand_jlt

    def handle_hlt(self):
        self.running = False
        self.pc += 1

    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
        self.pc += 3

    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def handle_nop(self):
        self.pc += 1

    def handle_mul(self):
        reg_num_1 = self.ram_read(self.pc + 1)
        reg_num_2 = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_num_1, reg_num_2)
        self.pc += 3

    def handle_add(self):
        reg_num_1 = self.ram_read(self.pc + 1)
        reg_num_2 = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_num_1, reg_num_2)
        self.pc += 3

    def handle_pop(self):
        # get register number to put value in
        reg_num = self.ram_read(self.pc + 1)
        # use stack pointer to get the value
        value = self.ram_read(self.sp)
        # put the value into the given register
        self.reg[reg_num] = value
        # now will increment the stack pointer:
        self.sp += 1
        # increment our stack pointer
        self.pc += 2

    def handle_push(self):
        # decriment the stack pointer
        self.sp -= 1
        # get the register number
        reg_num = self.ram_read(self.pc + 1)
        # get a value from the given register
        value = self.reg[reg_num]
        # put the value at the stack pointer address
        self.ram_write(self.sp, value)
        # increment program counter by 2
        self.pc += 2

    def handle_call(self):
        ### push command after CALL onto the stack
        return_address = self.pc + 2

        #### Get register number
        reg_num = self.ram[self.pc + 1]
        ### get the address to jump to, from the register
        subroutine_address = self.reg[reg_num]

        # push it on stack
        # decrement stack pointer
        # self.reg[7] -= 1
        self.sp -= 1
        # self.sp = self.reg[7]

        # this gets the address in the register for the top of stack
        top_of_stack_address = self.reg[self.sp]

        ### put return address on the stack
        self.ram_write(top_of_stack_address, return_address)

        ### then look at register, jump to that address
        self.pc = subroutine_address

    def handle_ret(self):

        # pop the return address off the stack
        top_of_stack_address = self.reg[self.sp]
        return_address = self.ram[top_of_stack_address]
        self.reg[self.sp] += 1
        # go to return address: set the pc to return address
        self.pc = return_address

    # ------------------Sprint Challenge----------------------------#

    def handle_cmp(self):
        pass

    def handle_jmp(self):
        pass

    def handle_jeq(self):
        pass

    def handle_jne(self):
        pass

    def handle_jgt(self):
        pass

    def handle_jge(self):
        pass

    def handle_jle(self):
        pass

    def handle_jlt(self):
        pass

    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        #    ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(filename) as f:
            for line in f:
                line = line.split("#")[0].strip()
                if line == "":
                    continue
                else:
                    self.ram[address] = int(line, 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[5] = 0
                self.fl[6] = 0
                self.fl[7] = 1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl[5] = 1
                self.fl[6] = 0
                self.fl[7] = 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl[5] = 0
                self.fl[6] = 1
                self.fl[7] = 0

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            IR = self.ram[self.pc]
            if IR not in self.branchtable:
                print("IR not in branchtable")
            self.branchtable[IR]()

