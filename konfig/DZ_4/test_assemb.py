import unittest
import yaml
import os
from assembler import *

class TestAssembler(unittest.TestCase):

    def setUp(self):
        self.input_file = "test_input.asm"
        self.output_bin = "test_output.bin"
        self.log_file = "test_log.yml"
        with open(self.input_file, 'w') as f:
            f.write("LOAD 5 123\n")
            f.write("READ 4 7\n")
            f.write("WRITE 2 6\n")
            f.write("MUL 3 2 8\n")

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_bin):
            os.remove(self.output_bin)
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_assemble(self):
        assemble(self.input_file, self.output_bin, self.log_file)
        self.assertTrue(os.path.exists(self.output_bin))

        with open(self.output_bin, 'rb') as f:
            binary_content = f.read()
        self.assertEqual(len(binary_content), 4 * 6)

        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, 'r') as f:
            log_data = yaml.safe_load(f)

        self.assertEqual(len(log_data), 4)
        self.assertEqual(log_data[0]['cmd_line'], "LOAD 5 123")
        self.assertTrue(log_data[0]['binary'].startswith("001"))
        self.assertTrue(log_data[1]['binary'].startswith("111"))
        self.assertTrue(log_data[2]['binary'].startswith("010"))
        self.assertTrue(log_data[3]['binary'].startswith("011"))

    def test_invalid_command(self):

        with open(self.input_file, 'w') as f:
            f.write("INVALID 5 123\n")
        with self.assertRaises(ValueError) as context:
            assemble(self.input_file, self.output_bin, self.log_file)
        
        self.assertIn("Unknown command: INVALID", str(context.exception))

if __name__ == '__main__':
    unittest.main()