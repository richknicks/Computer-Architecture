PRINT_TIM = 0b01
HALT = 0b10  # 2
PRINT_NUM = 0b11  # opcode 3
SAVE = 0b100
PRINT_REG = 0b101
ADD = 0b110
# save the number 99 into R2
# print whatever is inside R2
memory = [
    PRINT_TIM,  # <-- PC
    PRINT_TIM,
    PRINT_NUM,
    42,
    SAVE,
    2,  # Save in register 2
    99,  # number to save in register 2
    SAVE,
    3,  # Save in register 3
    1,  # number to save in register 3
    ADD,
    2,
    3,
    PRINT_REG,
    2,  # register to look in
    HALT,
]

# write a program to pull each command out of memory and execute
# We can loop over it!

registers = [0] * 8  # 8 general purpose registers, like variables, R0, R1, R2, ...R7
# [0,0,99,0,0,0,0,0]
# R0 - R7

pc = 0  # program counter, index of the current instruction, special purpose register
running = True
while running:
    command = memory[pc]  # Instruction register

    if command == PRINT_TIM:
        print("Tim!")
        pc += 1

    if command == HALT:
        running = False

    if command == PRINT_NUM:
        num_to_print = memory[pc + 1]
        print(num_to_print)
        pc += 1

    if command == SAVE:
        reg = memory[pc + 1]
        num_to_save = pc + 2
        registers[reg] = num_to_save
        pc += 2

    if command == PRINT_REG:
        reg = memory[pc + 1]
        print(registers[reg])
        pc += 1

    if command == ADD:

        pc += 1
