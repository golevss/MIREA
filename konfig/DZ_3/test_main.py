import unittest
from main import process_array, process_object, process_cons, process_value

class TestTranslator(unittest.TestCase):
    def test_process_array(self):
        arr = [1, 2, 3]
        expected = "(list 1 2 3 )"
        self.assertEqual(process_array(arr, 1), expected)

    def test_process_object(self):
        obj = {"key": 42, "values": [1, 2, 3]}
        expected = "struct {\n\tkey = 42,\n\tvalues = (list 1 2 3 )\n}"
        self.assertEqual(process_object(obj, 1), expected)

    def test_process_value(self):
        obj = {"key": 42}
        expected = "struct {\n\tkey = 42\n}"
        self.assertEqual(process_value(obj, 1), expected)

    def test_full_translation(self):
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