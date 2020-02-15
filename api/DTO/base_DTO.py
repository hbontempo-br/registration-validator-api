from datetime import date, datetime
from decimal import Decimal


class BaseDTO:
    def __init__(self, db_object: dict):
        self.db_object = db_object

    def generate_response_body(self):
        def process_generic(x):
            if isinstance(x, dict):
                return process_dict(x_dict=x)
            elif isinstance(x, list):
                return process_iterable(x_list=x)
            else:
                return process_value(value=x)

        def process_dict(x_dict: dict):
            return_dict = {}
            for key, value in x_dict.items():
                return_dict[key] = process_generic(value)
            return return_dict

        def process_iterable(x_list: list):
            return_list = []
            for x in x_list:
                return_list.append(process_generic(x))
            return return_list

        def process_value(value):
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, date):
                value = str(value)
            elif isinstance(value, Decimal):
                value = float(value)
            return value

        filtered_dto_dict = {
            k: v for k, v in self.db_object.items() if not k.startswith("_")
        }

        return process_generic(filtered_dto_dict)
