from typing import List


class CodeGeneratorBackend:
    """
    Class makes it easy to generate a python file and handle spacing
    Source: https://stackoverflow.com/questions/1364640/python-generating-python
    """

    def __init__(self, tab: str = "\t") -> None:
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self) -> str:
        return "".join(self.code)

    def write(self, string) -> None:
        self.code.append(self.tab * self.level + string)

    def indent(self) -> None:
        self.level = self.level + 1

    def dedent(self) -> None:
        if self.level == 0:
            raise SyntaxError("internal error in code generator")
        self.level = self.level - 1

    def create_code_string(self) -> str:
        """
        Combines all the line in self.code and creates a full str
        :return: full str for lines contained in self.code
        """
        return "\n".join(self.code)


class DataclassGenerator:
    """
    Class to generate data classes for python from arbitrary data structures
    """

    def __init__(self,
                 python_object: dict,
                 class_name: str,
                 class_description: str = "",
                 parent_class: bool = False,
                 add_defaults: bool=False,
                 enable_subclass: bool=True):
        """
        :param python_object: arbitrary python data structure such as a dict or list
        :param class_name: name of the data class to be generated
        :param class_description: description to be included with the class
        :param parent_class: set to true if this is meant to be the root class of a series of subclasses
        :param add_defaults: if true will add a default value for all the parameters of the classes. For data classes
        this looks like field(default_factory=str) for a string default for example
        :param enable_subclass: Makes the classes inherit the Subclass class... this makes the classes composable so
        you can actually make nested calls as designed
        """
        self.python_object = python_object
        self.class_name = class_name
        self.class_description = class_description
        self.parent_class = parent_class
        self.add_defaults = add_defaults
        self.enable_subclass = enable_subclass

    def generate_full_dataclass_file_str(self) -> str:
        """
        Generates a full file str that has imports as well as the dataclass itself
        :return: str with imports and dataclass
        """
        raise NotImplementedError

    def generate_parent_class_str(self) -> str:
        """
        This method generates a class and many subclasses from an arbitrary data structure supplied. Examples can be
        found in the integration tests.
        :return: str with executable python code that can be used as a class
        """
        classes: List[DataclassGenerator] = []
        type_overrides = {}
        for key, values in self.python_object.items():
            class_name = self.dash_case_to_camel(key)

            if type(values) == list and values:
                first_item = values[0]
                new_class_generator = DataclassGenerator(python_object=first_item, class_name=class_name,
                                                         parent_class=False, add_defaults=self.add_defaults)
                classes.append(new_class_generator)
                type_overrides[key] = f"List[{class_name}]"

            elif type(values) == dict and values:
                new_class_generator = DataclassGenerator(python_object=values, class_name=class_name,
                                                         parent_class=False, add_defaults=self.add_defaults)
                classes.append(new_class_generator)
                type_overrides[key] = class_name

        result_str = self.generate_dataclass_str(type_overrides=type_overrides) + "\n\n"

        for generator in classes:
            data_class_str = generator.generate_dataclass_str()
            result_str = data_class_str + result_str
            result_str += ""

        if self.enable_subclass:
            result_str += self.get_subclass_str()

        return result_str

    def generate_dataclass_str(self, type_overrides: dict = None) -> str:
        """
        Generates just the data class part of the str for the full thing. Ex:
        @dataclass
        class APIGatewayDataClass:
            id: str
            value: str
            customerId: str
            description: str
            enabled: bool
            createdDate: datetime.datetime
            stageKeys: List[str]
            tags: Dict[str, str]
        """
        if not type_overrides:
            type_overrides = {}

        codegenerator = CodeGeneratorBackend()
        codegenerator.write("\n\n@dataclass")
        if self.enable_subclass:
            class_string = f"class {self.class_name}(Subclass):"
        else:
            class_string = f"class {self.class_name}:"
        codegenerator.write(class_string)
        codegenerator.indent()

        if self.class_description:
            codegenerator.write('"""')
            codegenerator.write(f'{self.class_description}')
            codegenerator.write('"""')

        classes: List[DataclassGenerator] = []
        for field_name, value in self.python_object.items():
            clean_field_name = field_name.replace("-", "_")
            class_name = self.dash_case_to_camel(field_name)
            if field_name in type_overrides:
                new_line = f"{clean_field_name}: {type_overrides[field_name]}"
            elif type(value) == dict and value:
                new_class_generator = DataclassGenerator(python_object=value, class_name=class_name,
                                                         add_defaults=self.add_defaults)
                new_line = f"{clean_field_name}: {class_name}"
                classes.append(new_class_generator)
            else:
                val_type = DataclassGenerator.python_type_dataclass_type_converter(value)
                new_line = f"{clean_field_name}: {val_type}"
                if self.add_defaults:
                    new_line += DataclassGenerator.get_default_factory_string_for_type(value)
            codegenerator.write(new_line)

        data_class_str = codegenerator.create_code_string()

        for generator in classes:
            new_data_class = generator.generate_dataclass_str()
            data_class_str = new_data_class + data_class_str


        return data_class_str

    def generate_imports_str(self) -> str:
        """
        Generates the neccesary imports for a data class Ex:
        from dataclasses import dataclass
        import datetime
        from typing import List, Dict
        :return: str in above format
        """
        raise NotImplementedError

    @staticmethod
    def get_default_factory_string_for_type(value: object) -> str:
        """
        This function produces a default factory string for the type. This enables the option for allowing default values
        in data classes, this is useful for when you're not sure if every field will be used.
        :param value: any python object
        :return: valid default factory string i.e. ` = field(default_factory=list)` if given a list object
        """
        obj_type = DataclassGenerator.generic_type_converter(value)
        full_string = f" = field(default_factory={obj_type})"
        return full_string

    @staticmethod
    def simple_python_obj_to_type_string(obj: object) -> str:
        """
        This funciton just does very simple type -> string conversion. i.e. type(list) -> list instead of the more
        involved function below
        :param obj: any python object... Will default to a
        :return:
        """
        pass

    @staticmethod
    def python_type_dataclass_type_converter(obj: object) -> str:
        """
        This function takes in an arbitrary python object and returns a str version of it's type. Ex:
        "hello" -> str
        ["test", "test"] -> List[str]
        {"test_dict": 10} -> Dict[str, int]
        :param obj: arbitrary python object
        :return: str that is valid python code
        """
        if type(obj) == str:
            return "str"
        elif type(obj) == int:
            return "int"
        elif type(obj) == float:
            return "float"
        elif type(obj) == list:
            return DataclassGenerator.generate_list_type_str(obj)
        elif type(obj) == dict:
            return DataclassGenerator.generate_dict_type_str(obj)
        else:
            return DataclassGenerator.generic_type_converter(obj)

    @staticmethod
    def generate_list_type_str(list_obj: list, list_types_cutoff: int = 3) -> str:
        """
        Generates list type
        :param list_obj:
        :type list_obj:
        :return:
        """
        types = set()
        if len(list_obj) == 0:
            return "List"
        for item in list_obj:
            if type(item) == list:
                types.add("List")
            if type(item) == dict:
                types.add("Dict")
            else:
                types.add(DataclassGenerator.generic_type_converter(item))
            if len(types) > list_types_cutoff:
                return "List"
        if len(types) == 1:
            return f"List[{list(types)[0]}]"
        else:
            union_string = "List[Union["
            types = list(types)
            types.sort()
            for i, item in enumerate(types):
                union_string += item
                if i == len(types) - 1:
                    union_string += "]]"
                else:
                    union_string += ", "
        return union_string

    @staticmethod
    def generate_dict_type_str(dict_object: dict) -> str:
        """
        Generates a str for the dict ty
        :param dict_object:
        :type dict_object:
        :return:
        :rtype:
        """
        key_types = set()
        val_types = set()
        for key, val in dict_object.items():
            if type(key) == list:
                key_types.add("List")
            elif type(key) == dict:
                key_types.add("Dict")
            else:
                key_types.add(DataclassGenerator.generic_type_converter(key))
            if type(val) == list:
                val_types.add("List")
            elif type(val_types) == dict:
                val_types.add("dict")
            else:
                val_types.add(DataclassGenerator.generic_type_converter(val))
        if len(key_types) == 1:
            base_key_string = key_types.pop()
        elif len(key_types) > 3:
            base_key_string = "Any"
        else:
            base_key_string = ""
            for tp, i in enumerate(key_types):
                base_key_string += tp
                if i != len(key_types) - 1:
                    base_key_string += ","
        if len(val_types) == 1:
            base_val_string = val_types.pop()
        elif len(val_types) > 3:
            base_val_string = "Any"
        else:
            base_val_string = ""
            for i, tp in enumerate(val_types):
                base_val_string += tp
                if i != len(val_types) - 1:
                    base_val_string += ","
        full_dict_string = f"Dict[{base_key_string}, {base_val_string}]"
        return full_dict_string

    @staticmethod
    def generic_type_converter(obj: object) -> str:
        type_str = str(type(obj))
        type_str = type_str.replace("<", "").replace(">", "").replace("class", "").replace("'", "").replace(" ", "")
        return type_str

    @staticmethod
    def dash_case_to_camel(snake_str: str) -> str:
        result = ""
        next_cap = False
        for i, letter in enumerate(snake_str):
            if i == 0 or next_cap:
                result += letter.capitalize()
                next_cap = False
            elif letter == "-":
                next_cap = True
                continue
            else:
                result += letter
        return result

    @staticmethod
    def get_subclass_str() -> str:
        """
        This just gets the python code the subclass method... For now it's just hardcoded bc I'm doing it dynamically
        would be a bit difficult.
        :return: str of subclass that enables the nested calls
        """
        subclass_string = """
def convert_keys_to_snake_case(dict_to_fix: dict) -> dict:
    result = {}
    for key, value in dict_to_fix.items():
        new_key = key.replace("-", "_")
        result[new_key] = value
    return result

class SubClass:
    SUBCLASSES = {}

    @classmethod
    def init_from_json_dict(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        for key in new_dict:
            if key in cls.SUBCLASSES:
                if type(new_dict[key]) == dict:
                    new_dict[key] = convert_keys_to_snake_case(new_dict[key])
                    new_dict[key] = cls.SUBCLASSES[key].init_from_json_dict(new_dict[key])
                elif type(new_dict[key]) == list:
                    new_dict[key] = list(
                        map(lambda listDicts: cls.SUBCLASSES[key].init_from_json_dict(listDicts), new_dict[key]))
        try:
            return cls(**new_dict)
        except Exception as e:
            print("class that caused issue", cls)
            print("data struct that caused issue")
            pprint.pprint(e)
            pprint.pprint(new_dict)
        """
        return subclass_string




