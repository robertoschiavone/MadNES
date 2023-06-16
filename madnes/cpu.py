import numpy as np


class Cpu:
    def __init__(self):
        self.registers = {
            "PC": np.uint16,
            "S": np.uint8,
            "P": np.uint8,
            "A": np.uint8,
            "X": np.uint8,
            "Y": np.uint8,
        }

        for key in self.registers.keys():
            self.registers[key] = 0

        # unused flag: it is always set to 1
        self.unused_flag = 1

    @property
    def program_counter(self):
        return self.registers["PC"]

    @program_counter.setter
    def program_counter(self, value):
        self.registers["PC"] = value

    @property
    def stack_pointer(self):
        return self.registers["S"]

    @stack_pointer.setter
    def stack_pointer(self, value):
        self.registers["S"] = value

    @property
    def negative_flag(self):
        return self._get_flag(7)

    @negative_flag.setter
    def negative_flag(self, value: bool):
        self._set_flag(7, value)

    @property
    def overflow_flag(self):
        return self._get_flag(6)

    @overflow_flag.setter
    def overflow_flag(self, value: bool):
        self._set_flag(6, value)

    @property
    def unused_flag(self):
        return self._get_flag(5)

    @unused_flag.setter
    def unused_flag(self, value: bool):
        self._set_flag(5, value)

    @property
    def break_flag(self):
        return self._get_flag(4)

    @break_flag.setter
    def break_flag(self, value: bool):
        self._set_flag(4, value)

    @property
    def decimal_mode_flag(self):
        return self._get_flag(3)

    @decimal_mode_flag.setter
    def decimal_mode_flag(self, value: bool):
        self._set_flag(3, value)

    @property
    def interrupt_disable_flag(self):
        return (self.registers["P"] >> 2) & 1

    @interrupt_disable_flag.setter
    def interrupt_disable_flag(self, value: bool):
        self._set_flag(2, value)

    @property
    def zero_flag(self):
        return self._get_flag(1)

    @zero_flag.setter
    def zero_flag(self, value: bool):
        self._set_flag(1, value)

    @property
    def carry_flag(self):
        return self._get_flag(0)

    @carry_flag.setter
    def carry_flag(self, value: bool):
        self._set_flag(0, value)

    @property
    def accumulator(self):
        return self.registers["A"]

    @accumulator.setter
    def accumulator(self, value):
        self.registers["A"] = value

    @property
    def index_x(self):
        return self.registers["X"]

    @index_x.setter
    def index_x(self, value):
        self.registers["X"] = value

    @property
    def index_y(self):
        return self.registers["Y"]

    @index_y.setter
    def index_y(self, value):
        self.registers["Y"] = value

    def _get_flag(self, bit: np.uint8):
        return (self.registers["P"] >> bit) & 1

    def _set_flag(self, bit: np.uint8, value: bool):
        if value:
            self.registers["P"] |= 1 << bit
        else:
            self.registers["P"] &= ~(1 << bit)

    def __str__(self):
        msg = f"+{''.join(['-' for _ in range(68)])}+\n"
        msg += "|                                "
        msg += "CPU"
        msg += "                                 |\n"

        msg += f"+{''.join(['-' for _ in range(68)])}+\n"
        msg += "|   PC   |  S   |  A   |  X   |  Y   "
        msg += "| N | V | - | B | D | I | Z | C |\n"
        msg += f"+{''.join(['-' for _ in range(68)])}+\n"
        msg += f"| 0x{self.program_counter:04X} |"
        msg += f" 0x{self.stack_pointer:02X} |"
        msg += f" 0x{self.accumulator:02X} |"
        msg += f" 0x{self.index_x:02X} |"
        msg += f" 0x{self.index_y:02X} |"
        msg += f" {self.negative_flag:1d} |"
        msg += f" {self.overflow_flag:1d} |"
        msg += f" {self._get_flag(5):1d} |"
        msg += f" {self.break_flag:1d} |"
        msg += f" {self.decimal_mode_flag:1d} |"
        msg += f" {self.interrupt_disable_flag:1d} |"
        msg += f" {self.zero_flag:1d} |"
        msg += f" {self.carry_flag:1d} |\n"
        msg += f"+{''.join(['-' for _ in range(68)])}+\n"

        return msg
