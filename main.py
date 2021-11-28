import argparse
import json
from code_generator_backend import DataclassGenerator
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Provide a json file to make into a dataclass")
    parser.add_argument("-p", "--print", action="store_true", help="If flag is set will print to std out")
    parser.add_argument("-c", "--class-name", help="provide a name for the class")
    parser.add_argument("-d", "--description", required=False, default="", help="Provide a class description")
    return parser

def main() -> None:
    args = get_parser().parse_args()
    file = open(args.file, 'r')
    data = json.load(file)
    generator = DataclassGenerator(python_object=data, class_name=args.class_name, class_description=args.description)
    if args.print:
        print(generator.generate_dataclass_str())

if __name__ == '__main__':
    main()



