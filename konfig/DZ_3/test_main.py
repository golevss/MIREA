import unittest
import argparse
from io import StringIO
from unittest.mock import patch, mock_open

from main import *

class TestTranslator(unittest.TestCase):
    
    def test_process_array(self):
        input_data = [1, 2, {"key": 12}]
        expected_output = "(list 1 2 struct {\n\tkey = 12\n} )"
        self.assertEqual(process_array(input_data, 1), expected_output)
    
    def test_process_object(self):
        input_data = {"values": {"pi": 3.14, "e": 2.71}, "key": 12}
        expected_output = "struct {\n\tvalues = struct {\n\t\tpi = 3.14,\n\t\te = 2.71\n\t},\n\tkey = 12\n}"
        global consts
        consts = []
        self.assertEqual(process_object(input_data, 1), expected_output)

    def test_process_object_array(self):
        input_data = {"values": {"pi": 3.14, "e": 2.71}, "key": 12, "new_keys": [1,2,[3,4]]}
        expected_output = "struct {\n\tvalues = struct {\n\t\tpi = 3.14,\n\t\te = 2.71\n\t},\n\tkey = 12,\n\tnew_keys = (list 1 2 (list 3 4 ) )\n}"
        global consts
        consts = []
        self.assertEqual(process_object(input_data, 1), expected_output)

    def test_process_object_array_2(self):
        input_data = {"values": {"pi": 3.14, "e": 2.71}, "key": 12, "new_keys": [1, 2, {"key": 12}]}
        expected_output = "struct {\n\tvalues = struct {\n\t\tpi = 3.14,\n\t\te = 2.71\n\t},\n\tkey = 12,\n\tnew_keys = (list 1 2 struct {\n\t\tkey = 12\n\t} )\n}"
        global consts
        consts = []
        self.assertEqual(process_object(input_data, 1), expected_output)

    def test_process_object_array_coms(self):
        input_data = {"constants": {"key": 12}, "values": {"pi": 3.14, "e": 2.71}, "key": 12, "coments": {"key" : 12}}
        expected_output = "\ key = 12\ndef key := 12;\nstruct {\n\tvalues = struct {\n\t\tpi = 3.14,\n\t\te = 2.71\n\t},\n\tkey = 12\n}"
        global consts
        consts = []
        self.assertEqual(process_object(input_data, 1), expected_output)
    
    def test_process_cons(self):
        input_data = {"pi": 3.14, "e": 2.71}
        expected_output = "def pi := 3.14;\ndef e := 2.71;\n"
        global consts
        consts = []
        self.assertEqual(process_cons(input_data), expected_output)

    def test_process_coms(self):
        input_data = {"author": 12, "date": 11}
        expected_output = '\ author = 12\n\ date = 11\n'
        self.assertEqual(process_coms(input_data), expected_output)

    def test_process_value_int(self):
        self.assertEqual(process_value(42, 1), "42")

    def test_process_value_list(self):
        input_data = [1, 2, 3]
        expected_output = "(list 1 2 3 )"
        self.assertEqual(process_array(input_data, 1), expected_output)
    
    def test_process_value_dict(self):
        input_data = {"key": 12}
        expected_output = "struct {\n\tkey = 12\n}"
        self.assertEqual(process_object(input_data, 1), expected_output)
    
    def test_process_value_unsupported_type(self):
        with self.assertRaises(ValueError):
            process_value(set([1, 2, 3]), 1)
    
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_file_not_found(self, mock_stdout, mock_open):
        input_file = "nonexistent.json"
        output_file = "output.txt"
        with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(input=input_file, output=output_file)):
            with self.assertRaises(SystemExit):
                main(input_file, output_file)
            self.assertIn("Error:", mock_stdout.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": 12}')
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_success(self, mock_stdout, mock_open):
        input_file = "input.json"
        output_file = "output.txt"
        with patch("main.process_object", return_value="struct {\n\tkey = 12\n}"):
            main(input_file, output_file)
        self.assertIn("Translation completed successfully.", mock_stdout.getvalue())
        mock_open().write.assert_called_once_with("struct {\n\tkey = 12\n}")

if __name__ == "__main__":
    unittest.main()
