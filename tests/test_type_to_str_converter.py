from code_generator_backend import DataclassGenerator
from unittest import TestCase
import datetime

class TestPrimitives(TestCase):

    def test_basics(self):
        inputs = ["test", 10.0, 10]
        expected_outputs = ["str", "float", "int"]
        for i, output in zip(inputs, expected_outputs):
            actual_output = DataclassGenerator.python_type_dataclass_type_converter(i)
            self.assertEqual(output, actual_output)

    def test_list_str(self):
        input_list = ["this", "is", "a", "list of strings"]
        expected_output = "List[str]"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_list)
        self.assertEqual(actual_output, expected_output)

    def test_dict_str(self):
        input_dict = {"String":"value", "String2":"Value2"}
        expected_output = "Dict[str, str]"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_dict)
        self.assertEqual(actual_output, expected_output)

    def test_dict_int_str(self):
        input_dict = {1:"test", 2:"tes2", 3:"test3"}
        expected_output = "Dict[int, str]"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_dict)
        self.assertEqual(actual_output, expected_output)

    def test_datetime(self):
        input_date = datetime.datetime(day=10, month=10, year=2017)
        expected_outout = "datetime.datetime"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_date)
        self.assertEqual(actual_output, expected_outout)

    def test_empty_list(self):
        input_data = []
        expected_output = "List"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_data)
        self.assertEqual(actual_output, expected_output)

class TestUnionTypes(TestCase):

    def test_union_list(self):
        input_list = ["string", 10]
        expected_output = "List[Union[int, str]]"
        actual_ouput = DataclassGenerator.python_type_dataclass_type_converter(input_list)
        self.assertEqual(actual_ouput, expected_output)

    def test_4_types_list(self):
        input_list = ["test", 10, 10.0, {}]
        expected_ouput = "List"
        actual_output = DataclassGenerator.python_type_dataclass_type_converter(input_list)
        self.assertEqual(actual_output, expected_ouput)
