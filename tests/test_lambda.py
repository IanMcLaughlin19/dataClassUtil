import pprint
import unittest
import boto3
import requests
import json

API_URL = "https://2otbdflyea.execute-api.us-east-1.amazonaws.com/hello"

class TestLambdaAPI(unittest.TestCase):
    """
    This runs some tests against the API endpoint to ensure it is working as expected
    """
    INPUT_TEXT = """
{   "application_transaction": "test",
    "close_rewards": 0,
    "closing_amount": 0,
    "confirmed_round": 20330180,
    "fee": 1000,
    "first_valid": 20330176,
    "genesis_hash": "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=",
    "genesis_id": "mainnet-v1.0",
    "group": "P3G/1RWtsvDlSivdPg0y9Bsa51a+LYqmp2Oj9xFORBQ=",
    "id": "PRYG5NCMHKJ67YED7PPBRRIN5IH4BMFSW6EDXFY4J7SAJDXMZUZQ"
}
        """
    def test_basic_json(self):
        """
        Passes a valid json file as a string to the lambda and makes sure we get a 200 response
        """
        json_text = self.INPUT_TEXT
        req_lambda = requests.post(API_URL, params={"text": json_text})

        json_test = req_lambda.json()
        pprint.pprint(req_lambda.json())
        self.assertEqual(req_lambda.status_code, 200)

    def test_equal_json(self):
        """
        Checks that we get the correct expected result from inputting a basic non nested json string
        """
        json_text = self.INPUT_TEXT
        req_lambda = requests.post(API_URL, params={"text": json_text})
        self.maxDiff = None
        expected_output ="""

@dataclass
class None(Subclass):
	application_transaction: str
	close_rewards: int
	closing_amount: int
	confirmed_round: int
	fee: int
	first_valid: int
	genesis_hash: str
	genesis_id: str
	group: str
	id: str


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
            pprint.pprint(new_dict)"""
        actual_output = req_lambda.json()['text']
        self.assertEqual(expected_output, actual_output)