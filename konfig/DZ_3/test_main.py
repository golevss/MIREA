import unittest
from main import process_array, process_object, process_cons, process_value

class TestTranslator(unittest.TestCase):
    def test_process_array(self):
        arr = [1, 2, 3]
        expected = "(list 1 2 3 )"
        self.assertEqual(process_array(arr, 1), expected)
    def test_process_array_2(self):
        arr_nested = [1, [2, 3], 4]
        expected_nested = "(list 1 (list 2 3 ) 4 )"
        self.assertEqual(process_array(arr_nested, 1), expected_nested)
    def test_process_array_3(self):
        arr_nested = [[1,2], [3, 4]]
        expected_nested = "(list (list 1 2 ) (list 3 4 ) )"
        self.assertEqual(process_array(arr_nested, 1), expected_nested)

    def test_process_cons(self):
        arr_nested = {"constants":{"a": 1, "b": 2}, "c":5}
        expected_nested = "def a := 1;\ndef b := 2;\nstruct {\n\tc = 5\n}"
        self.assertEqual(process_object(arr_nested,1), expected_nested)
    def test_process_cons_2(self):
        arr_nested = {"constants":{"a": [1,2,3,4], "b": 2}, "c":5}
        expected_nested = "def a := (list 1 2 3 4 );\ndef b := 2;\nstruct {\n\tc = 5\n}"
        self.assertEqual(process_object(arr_nested,1), expected_nested)

    def test_process_object(self):
        obj = {"key": 42, "values": [1, 2, 3]}
        expected = "struct {\n\tkey = 42,\n\tvalues = (list 1 2 3 )\n}"
        self.assertEqual(process_object(obj, 1), expected)
    def test_process_object_2(self):
        obj_nested = {"outer": {"inner": 1}}
        expected_nested = "struct {\n\touter = struct {\n\t\tinner = 1\n\t}\n}"
        self.assertEqual(process_object(obj_nested, 1), expected_nested)
    def test_process_object_3(self):
        obj_nested = {"outer": {"inner": 1}, "val":{"var":2}}
        expected_nested = "struct {\n\touter = struct {\n\t\tinner = 1\n\t},\n\tval = struct {\n\t\tvar = 2\n\t}\n}"
        self.assertEqual(process_object(obj_nested, 1), expected_nested)

    def test_process_value(self):
        obj = {"key": 42}
        expected = "struct {\n\tkey = 42\n}"
        self.assertEqual(process_value(obj, 1), expected)
    def test_process_value_2(self):
        obj = {"key_a": 42,"key_b":43,"key_c":44,"key_d":45}
        expected = "struct {\n\tkey_a = 42,\n\tkey_b = 43,\n\tkey_c = 44,\n\tkey_d = 45\n}"
        self.assertEqual(process_value(obj, 1), expected)
    def test_process_value_3(self):
        obj = {"key_a": [1,2],"key_b": [3,4]}
        expected = "struct {\n\tkey_a = (list 1 2 ),\n\tkey_b = (list 3 4 )\n}"
        self.assertEqual(process_value(obj, 1), expected)

    def test_full_file(self):
        json_data = {
            "constants": {"const1": 100},
            "data": {
                "keya": 42,
                "keyb": [1, 2, {"nested": 3}]
            }
        }
        expected = (
            "def const1 := 100;\n"
            "struct {\n"
            "\tdata = struct {\n"
            "\t\tkeya = 42,\n"
            "\t\tkeyb = (list 1 2 struct {\n"
            "\t\t\tnested = 3\n"
            "\t\t} )\n"
            "\t}\n"
            "}"
        )
        self.assertEqual(process_object(json_data, 1), expected)


if __name__ == '__main__':
    unittest.main()