import sys

import numpy as np

from collections import deque

from madnes.cpu import Cpu

np.set_printoptions(threshold=sys.maxsize)


def get_bit(data, bit):
    return (data >> bit) & 1


def process_opcode(opcodes: deque, cpu, memory):
    while len(opcodes):
        opcode = opcodes.popleft()

        match opcode:
            # BRK - Force Interrupt
            # Addressing Mode: Implied
            # Flags: -
            case 0x00:
                cpu.break_flag = 1
            # ORA - Logical Inclusive OR
            # Addresing Mode: Indexed Indirect
            # Flags: Z, N
            case 0x01:
                if cpu.accumulator == 0:
                    cpu.zero_flag = 1
                address = opcodes.popleft()
                cpu.accumulator = cpu.accumulator | memory[address + cpu.index_x]
                if get_bit(cpu.accumulator, 7):
                    cpu.negative_flag = 1
                cpu.program_counter += 1
            # ORA - Logical Inclusive OR
            # Addressing Mode: Zero Page
            # Flags: Z, N
            case 0x05:
                if cpu.accumulator == 0:
                    cpu.zero_flag = 1
                address = opcodes.popleft()
                cpu.accumulator = cpu.accumulator | memory[address]
                if get_bit(cpu.accumulator, 7):
                    cpu.negative_flag = 1
                cpu.program_counter += 1
            # ASL - Arithmetic Shift Left
            # Addressing Mode: Zero Page
            # Flags: C, Z, N
            case 0x06:
                cpu.carry_flag = get_bit(cpu.accumulator, 7)
                cpu.accumulator <<= 1
            # PHP - PHP - Push Processor Status
            # Addressing Mode: Implied
            # Flags: -
            case 0x08:
                pass
            case _:
                pass

        cpu.program_counter += 1
        print(cpu)


if __name__ == "__main__":
    cpu = Cpu()
    print(cpu)
    memory = np.random.randint(0, high=255, size=0x10000, dtype=np.uint8)
    opcodes = deque([0x00, 0x01, 0x05, 0x06])

    process_opcode(opcodes, cpu, memory)

# // ORA #$NN                Immediate                 - Z- - - - N
#         case 0x09:
#             break;
# // ASL A                Accumulator                 CZ- - - - N
#         case 0x0A:
#             break;
# // ORA $NNNN                Absolute                 - Z- - - - N
#         case 0x0d:
#             break;
# // ASL $NNNN                Absolute                 CZ- - - - N
#         case 0x0E:
#             break;
# // BPL $NN                Relative                 - - - - - - -
#         case 0x10:
#             break;
# // ORA ($NN),Y                Indirect Indexed                 - Z- - - - N
#         case 0x11:
#             break;
# // ORA $NN,X                Zero Page,X                 - Z- - - - N
#         case 0x15:
#             break;
# // ASL $NN,X                Zero Page,X                 CZ- - - - N
#         case 0x16:
#             break;
# // CLC                 Implied                 C- - - - - -
#         case 0x18:
#             break;
# // ORA $NNNN,Y                Absolute,Y                 - Z- - - - N
#         case 0x19:
#             break;
# // ORA $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0x1d:
#             break;
# // ASL $NNNN,X                Absolute,X                 CZ- - - - N
#         case 0x1E:
#             break;
# // JSR $NNNN                Absolute                 - - - - - - -
#         case 0x20:
#             break;
# // AND ($NN,X)                Indexed Indirect                 - Z- - - - N
#         case 0x21:
#             break;
# // BIT $NN                Zero Page                 - Z- - - VN
#         case 0x24:
#             break;
# // AND $NN                Zero Page                 - Z- - - - N
#         case 0x25:
#             break;
# // ROL $NN                Zero Page                 CZ- - - - N
#         case 0x26:
#             break;
# // PLP                 Implied                 CZIDBVN
#         case 0x28:
#             break;
# // AND #$NN                Immediate                 - Z- - - - N
#         case 0x29:
#             break;
# // ROL A                Accumulator                 CZ- - - - N
#         case 0x2A:
#             break;
# // BIT $NNNN                Absolute                 - Z- - - VN
#         case 0x2C:
#             break;
# // AND $NNNN                Absolute                 - Z- - - - N
#         case 0x2d:
#             break;
# // ROL $NNNN                Absolute                 CZ- - - - N
#         case 0x2E:
#             break;
# // BMI $NN                Relative                 - - - - - - -
#         case 0x30:
#             break;
# // AND ($NN),Y                Indirect Indexed                 - Z- - - - N
#         case 0x31:
#             break;
# // AND $NN,X                Zero Page,X                 - Z- - - - N
#         case 0x35:
#             break;
# // ROL $NN,X                Zero Page,X                 CZ- - - - N
#         case 0x36:
#             break;
# // SEC                 Implied                 C- - - - - -
#         case 0x38:
#             break;
# // AND $NNNN,Y                Absolute,Y                 - Z- - - - N
#         case 0x39:
#             break;
# // AND $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0x3d:
#             break;
# // ROL $NNNN,X                Absolute,X                 CZ- - - - N
#         case 0x3E:
#             break;
# // RTI                 Implied                 - - - - - - -
#         case 0x40:
#             break;
# // EOR ($NN,X)                Indexed Indirect                 - Z- - - - N
#         case 0x41:
#             break;
# // EOR $NN                Zero Page                 - Z- - - - N
#         case 0x45:
#             break;
# // LSR $NN                Zero Page                 CZ- - - - N
#         case 0x46:
#             break;
# // PHA                 Implied                 - - - - - - -
#         case 0x48:
#             break;
# // EOR #$NN                Immediate                 - Z- - - - N
#         case 0x49:
#             break;
# // LSR A                Accumulator                 CZ- - - - N
#         case 0x4A:
#             break;
# // JMP $NNNN                Absolute                 - - - - - - -
#         case 0x4C:
#             break;
# // EOR $NNNN                Absolute                 - Z- - - - N
#         case 0x4d:
#             break;
# // LSR $NNNN                Absolute                 CZ- - - - N
#         case 0x4E:
#             break;
# // BVC $NN                Relative                 - - - - - - -
#         case 0x50:
#             break;
# // EOR ($NN),Y                Indirect Indexed                 - Z- - - - N
#         case 0x51:
#             break;
# // EOR $NN,X                Zero Page,X                 - Z- - - - N
#         case 0x55:
#             break;
# // LSR $NN,X                Zero Page,X                 CZ- - - - N
#         case 0x56:
#             break;
# // CLI                 Implied                 - - I- - - -
#         case 0x58:
#             break;
# // EOR $NNNN,Y                Absolute,Y                 - Z- - - - N
#         case 0x59:
#             break;
# // EOR $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0x5d:
#             break;
# // LSR $NNNN,X                Absolute,X                 CZ- - - - N
#         case 0x5E:
#             break;
# // RTS                 Implied                 - - - - - - -
#         case 0x60:
#             break;
# // ADC ($NN,X)                Indexed Indirect                 CZ- - - VN
#         case 0x61:
#             break;
# // ADC $NN                Zero Page                 CZ- - - VN
#         case 0x65:
#             break;
# // ROR $NN                Zero Page                 CZ- - - - N
#         case 0x66:
#             break;
# // PLA                 Implied                 - Z- - - - N
#         case 0x68:
#             break;
# // ADC #$NN                Immediate                 CZ- - - VN
#         case 0x69:
#             break;
# // ROR A                Accumulator                 CZ- - - - N
#         case 0x6A:
#             break;
# // JMP $NN                Indirect                 - - - - - - -
#         case 0x6C:
#             break;
# // ADC $NNNN                Absolute                 CZ- - - VN
#         case 0x6d:
#             break;
# // ROR $NNNN,X                Absolute,X                 CZ- - - - N
#         case 0x6E:
#             break;
# // BVS $NN                Relative                 - - - - - - -
#         case 0x70:
#             break;
# // ADC ($NN),Y                Indirect Indexed                 CZ- - - VN
#         case 0x71:
#             break;
# // ADC $NN,X                Zero Page,X                 CZ- - - VN
#         case 0x75:
#             break;
# // ROR $NN,X                Zero Page,X                 CZ- - - - N
#         case 0x76:
#             break;
# // SEI                 Implied                 - - I- - - -
#         case 0x78:
#             break;
# // ADC $NNNN,Y                Absolute,Y                 CZ- - - VN
#         case 0x79:
#             break;
# // ADC $NNNN,X                Absolute,X                 CZ- - - VN
#         case 0x7d:
#             break;
# // ROR $NNNN                Absolute                 CZ- - - - N
#         case 0x7E:
#             break;
# // STA ($NN,X)                Indexed Indirect                 - - - - - - -
#         case 0x81:
#             break;
# // STY $NN                Zero Page                 - - - - - - -
#         case 0x84:
#             break;
# // STA $NN                Zero Page                 - - - - - - -
#         case 0x85:
#             break;
# // STX $NN                Zero Page                 - - - - - - -
#         case 0x86:
#             break;
# // DEY                 Implied                 - Z- - - - N
#         case 0x88:
#             break;
# // TXA                 Implied                 - Z- - - - N
#         case 0x8A:
#             break;
# // STY $NNNN                Absolute                 - - - - - - -
#         case 0x8C:
#             break;
# // STA $NNNN                Absolute                 - - - - - - -
#         case 0x8d:
#             break;
# // STX $NNNN                Absolute                 - - - - - - -
#         case 0x8E:
#             break;
# // BCC $NN                Relative                 - - - - - - -
#         case 0x90:
#             break;
# // STA ($NN),Y                Indirect Indexed                 - - - - - - -
#         case 0x91:
#             break;
# // STY $NN,X                Zero Page,X                 - - - - - - -
#         case 0x94:
#             break;
# // STA $NN,X                Zero Page,X                 - - - - - - -
#         case 0x95:
#             break;
# // STX $NN,Y                Zero Page,Y                 - - - - - - -
#         case 0x96:
#             break;
# // TYA                 Implied                 - Z- - - - N
#         case 0x98:
#             break;
# // STA $NNNN,Y                Absolute,Y                 - - - - - - -
#         case 0x99:
#             break;
# // TXS                 Implied                 - - - - - - -
#         case 0x9A:
#             break;
# // STA $NNNN,X                Absolute,X                 - - - - - - -
#         case 0x9d:
#             break;
# // LDY #$NN                Immediate                 - Z- - - - N
#         case 0xA0:
#             break;
# // LDA ($NN,X)                Indexed Indirect                 - Z- - - - N
#         case 0xA1:
#             break;
# // LDX #$NN                Immediate                 - Z- - - - N
#         case 0xA2:
#             break;
# // LDY $NN                Zero Page                 - Z- - - - N
#         case 0xA4:
#             break;
# // LDA $NN                Zero Page                 - Z- - - - N
#         case 0xA5:
#             break;
# // LDX $NN                Zero Page                 - Z- - - - N
#         case 0xA6:
#             break;
# // TAY                 Implied                 - Z- - - - N
#         case 0xA8:
#             break;
# // LDA #$NN                Immediate                 - Z- - - - N
#         case 0xA9:
#             break;
# // TAX                 Implied                 - Z- - - - N
#         case 0xAA:
#             break;
# // LDY $NNNN                Absolute                 - Z- - - - N
#         case 0xAC:
#             break;
# // LDA $NNNN                Absolute                 - Z- - - - N
#         case 0xAd:
#             break;
# // LDX $NNNN                Absolute                 - Z- - - - N
#         case 0xAE:
#             break;
# // BCS $NN                Relative                 - - - - - - -
#         case 0xB0:
#             break;
# // LDA ($NN),Y                Indirect Indexed                 - Z- - - - N
#         case 0xB1:
#             break;
# // LDY $NN,X                Zero Page,X                 - Z- - - - N
#         case 0xB4:
#             break;
# // LDA $NN,X                Zero Page,X                 - Z- - - - N
#         case 0xB5:
#             break;
# // LDX $NN,Y                Zero Page,Y                 - Z- - - - N
#         case 0xB6:
#             break;
# // CLV                 Implied                 - - - - - V-
#         case 0xB8:
#             break;
# // LDA $NNNN,Y                Absolute,Y                 - Z- - - - N
#         case 0xB9:
#             break;
# // TSX                 Implied                 - Z- - - - N
#         case 0xBA:
#             break;
# // LDY $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0xBC:
#             break;
# // LDA $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0xBd:
#             break;
# // LDX $NNNN,Y                Absolute,Y                 - Z- - - - N
#         case 0xBE:
#             break;
# // CPY #$NN                Immediate                 CZ- - - - N
#         case 0xC0:
#             break;
# // CMP ($NN,X)                Indexed Indirect                 CZ- - - - N
#         case 0xC1:
#             break;
# // CPY $NN                Zero Page                 CZ- - - - N
#         case 0xC4:
#             break;
# // CMP $NN                Zero Page                 CZ- - - - N
#         case 0xC5:
#             break;
# // DEC $NN                Zero Page                 - Z- - - - N
#         case 0xC6:
#             break;
# // INY                 Implied                 - Z- - - - N
#         case 0xC8:
#             break;
# // CMP #$NN                Immediate                 CZ- - - - N
#         case 0xC9:
#             break;
# // DEX                 Implied                 - Z- - - - N
#         case 0xCA:
#             break;
# // CPY $NNNN                Absolute                 CZ- - - - N
#         case 0xCC:
#             break;
# // CMP $NNNN                Absolute                 CZ- - - - N
#         case 0xCd:
#             break;
# // DEC $NNNN                Absolute                 - Z- - - - N
#         case 0xCE:
#             break;
# // BNE $NN                Relative                 - - - - - - -
#         case 0xd0:
#             break;
# // CMP ($NN),Y                Indirect Indexed                 CZ- - - - N
#         case 0xd1:
#             break;
# // CMP $NN,X                Zero Page,X                 CZ- - - - N
#         case 0xd5:
#             break;
# // DEC $NN,X                Zero Page,X                 - Z- - - - N
#         case 0xd6:
#             break;
# // CLD                 Implied                 - - - D- - -
#         case 0xd8:
#             break;
# // CMP $NNNN,Y                Absolute,Y                 CZ- - - - N
#         case 0xd9:
#             break;
# // CMP $NNNN,X                Absolute,X                 CZ- - - - N
#         case 0xdd:
#             break;
# // DEC $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0xdE:
#             break;
# // CPX #$NN                Immediate                 CZ- - - - N
#         case 0xE0:
#             break;
# // SBC ($NN,X)                Indexed Indirect                 CZ- - - VN
#         case 0xE1:
#             break;
# // CPX $NN                Zero Page                 CZ- - - - N
#         case 0xE4:
#             break;
# // SBC $NN                Zero Page                 CZ- - - VN
#         case 0xE5:
#             break;
# // INC $NN                Zero Page                 - Z- - - - N
#         case 0xE6:
#             break;
# // INX                 Implied                 - Z- - - - N
#         case 0xE8:
#             break;
# // SBC #$NN                Immediate                 CZ- - - VN
#         case 0xE9:
#             break;
# // NOP                 Implied                 - - - - - - -
#         case 0xEA:
#             break;
# // CPX $NNNN                Absolute                 CZ- - - - N
#         case 0xEC:
#             break;
#             // SBC $NNNN                Absolute                 CZ- - - VN
#         case 0xEd:
#             break;
#             // INC $NNNN                Absolute                 - Z- - - - N
#         case 0xEE:
#             break;
#             // BEQ $NN                Relative                 - - - - - - -
#         case 0xF0:
#             break;
#             // SBC ($NN),Y                Indirect Indexed                 CZ- - - VN
#         case 0xF1:
#             break;
#             // SBC $NN,X                Zero Page,X                 CZ- - - VN
#         case 0xF5:
#             break;
#             // INC $NN,X                Zero Page,X                 - Z- - - - N
#         case 0xF6:
#             break;
#             // SED                 Implied                 - - - D- - -
#         case 0xF8:
#             break;
#             // SBC $NNNN,Y                Absolute,Y                 CZ- - - VN
#         case 0xF9:
#             break;
#             // SBC $NNNN,X                Absolute,X                 CZ- - - VN
#         case 0xFd:
#             break;
#             // INC $NNNN,X                Absolute,X                 - Z- - - - N
#         case 0xFE:
#             break;
#     }
#     state->pc += 1;
# }
#
#
# int main() {
#     printf("Hello, World!\n");
#     return 0;
# }
#
