import unittest

from madnes.cpu import Cpu
from madnes.main import process_opcode


class TestOpcodes(unittest.TestCase):

    def test_0x00(self):
        cpu = Cpu()
        self.assertEqual(cpu.break_flag, 0)
        process_opcode(0x00, cpu, None)
        self.assertEqual(cpu.break_flag, 1)

    def test_0x01(self):
        cpu = Cpu()
        self.assertEqual(cpu.break_flag, 0)
        process_opcode(0x00, cpu, None)
        self.assertEqual(cpu.break_flag, 1)

        cpu = Cpu()
        self.assertEqual(cpu.break_flag, 0)
        process_opcode(0x00, cpu, None)
        self.assertEqual(cpu.break_flag, 1)


if __name__ == '__main__':
    unittest.main()
