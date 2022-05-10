import json
import pprint
from code_generator_backend import DataclassGenerator

def lambda_handler(event, context):
    """
    l
    """
    try:
        args = event['queryStringParameters']
        print("ARGS")
        pprint.pprint(args, indent=4)
        json_text = args['text']
        class_name = args['class_name'] if 'class_name' in args else None
        enable_subclass = args['enable_subclass'] if 'enable_subclass' in args else True
        json_object = json.loads(json_text)
        generator = DataclassGenerator(python_object=json_object, class_name=class_name, enable_subclass=enable_subclass)
        dataclass_string = generator.generate_parent_class_str()
        return {
            'statusCode': 200,
            'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH"
            },
            'body': json.dumps({"text": dataclass_string})
        }
    except Exception as e:
        print("This got reached!1")
        try:
            return {"Error": str(e), "event": str(event)}
        except Exception as ee:
            print("This got reached!2")
            return {"Error": ee}