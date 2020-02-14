from __future__ import annotations

import re
from typing import NoReturn
from typing import TYPE_CHECKING

from api.resources.base_resource import BaseResource
from api.schemas.api_schema import get_specification
import falcon
from utils.errors import InternalError
from utils.errors import request_error_handler
from utils.schema_validator import validate_schema
from validate_docbr import CPF

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response

VALIDATOR_SCHEMA_DICT = get_specification(schema_name="ValidatorRequest")


class Validator(BaseResource):
    @request_error_handler
    def on_get_with_social_security_number(
        self, req: Request, res: Response, social_security_number: str = None
    ) -> NoReturn:
        pass

    @request_error_handler
    @falcon.before(action=validate_schema, schema_dict=VALIDATOR_SCHEMA_DICT)
    def on_post(self, req: Request, res: Response) -> NoReturn:
        body = req.media
        phone = body.get("phone")
        social_security_number = body.get("social_security_number")

        phone_validation = self.__validate_phone(phone=phone)
        social_security_number_validation = self.__validate_social_security_number(
            social_security_number=social_security_number
        )

        success = phone_validation and social_security_number_validation
        body["success"] = success

        if success:
            self.generate_response(res=res, status_code=200, body_dict=body)
        else:
            msg = self.__generate_error_msg(
                phone_validation=phone_validation,
                social_security_number_validation=social_security_number_validation,
            )
            body["msg"] = msg
            response_body = {"success": success, "msg": msg}
            self.generate_response(res=res, status_code=400, body_dict=response_body)

        # Save to database

    @staticmethod
    def __validate_phone(phone: str) -> bool:
        regex_pattern = "^\([1-9]{2}\)(?:[2-8]|9[1-9])[0-9]{7}$"  # noqa: W605
        match = re.fullmatch(pattern=regex_pattern, string=phone)
        return bool(match)

    @staticmethod
    def __validate_social_security_number(social_security_number: str) -> bool:
        cpf = CPF()
        return cpf.validate(doc=social_security_number)

    @staticmethod
    def __generate_error_msg(
        phone_validation: bool, social_security_number_validation: bool
    ) -> str:
        msg_dict = {
            (False, False): "Invalid social_security_number and phone",
            (False, True): "Invalid  phone",
            (True, False): "Invalid social_security_number",
        }
        validation_tuple = (phone_validation, social_security_number_validation)
        return_msg = msg_dict.get(validation_tuple)
        if not return_msg:
            raise InternalError().http()
        return return_msg
