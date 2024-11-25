import unittest
import yaml
import os
from interpreter import *

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.binary_file = "test_binary.bin"
        self.output_file = "test_output.yml"
        self.memory_range = (0, 10)

        with open(self.binary_file, 'wb') as f:
            instr1 = (1 << 46) | (5 << 40) | (123 << 27)
            instr2 = (0 << 46) | (4 << 40) | (7 << 27)
            instr3 = (2 << 46) | (2 << 13) | (6 << 7)
            instr4 = (3 << 46) | (3 << 40) | (2 << 35) | (8 << 3)

            f.write(instr1.to_bytes(6, byteorder='big'))
            f.write(instr2.to_bytes(6, byteorder='big'))
            f.write(instr3.to_bytes(6, byteorder='big'))
            f.write(instr4.to_bytes(6, byteorder='big'))

    def tearDown(self):
        if os.path.exists(self.binary_file):
            os.remove(self.binary_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_din_to_str(self):
        result = din_to_str(self.binary_file)
        self.assertEqual(len(result), 24)

    def test_interpret(self):
        interpret(self.binary_file, self.output_file, self.memory_range)

        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, 'r') as f:
            output_data = yaml.safe_load(f)

        self.assertIn('memory', output_data)
        self.assertEqual(len(output_data['memory']), self.memory_range[1] - self.memory_range[0])

if __name__ == "__main__":
    unittest.main()