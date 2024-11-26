import unittest
import yaml
import os
from interpreter import *

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.binary_file = 'test_binary.bin'
        self.output_file = 'test_output.yml'
        self.memory_range = (0, 10)

        with open(self.binary_file, 'wb') as f:
            instr1 = (1 << 45) | (1 << 40) | (42 << 27)
            instr2 = (7 << 45) | (2 << 40) | (1 << 27)
            instr3 = (2 << 45) | (3 << 13) | (2 << 7)
            instr4 = (3 << 45) | (4 << 40) | (3 << 35) | (2 << 3)

            for instr in [instr1, instr2, instr3, instr4]:
                f.write(instr.to_bytes(6, byteorder='big'))

    def tearDown(self):
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_din_to_str(self):
        binary_data = din_to_str(self.binary_file)
        self.assertEqual(len(binary_data), 24)

    def test_interpret(self):
        interpret(self.binary_file, self.output_file, self.memory_range)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, 'r') as f:
            output_data = yaml.safe_load(f)

        self.assertIn('memory', output_data)
        self.assertEqual(len(output_data['memory']), self.memory_range[1] - self.memory_range[0])
        self.assertEqual(output_data['memory'], [0] * 10)

    def test_invalid_instruction(self):
        with open(self.binary_file, 'wb') as f:
            invalid_instr = (8 << 45)
        with self.assertRaises(OverflowError):
            f.write(invalid_instr.to_bytes(6, byteorder='big'))
            interpret(self.binary_file, self.output_file, self.memory_range)


if __name__ == '__main__':
    unittest.main()
