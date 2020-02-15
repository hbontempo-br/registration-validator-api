from __future__ import annotations

import re
from typing import NoReturn
from typing import TYPE_CHECKING

from api.resources.base_resource import BaseResource
from api.schemas.api_schema import get_specification
import falcon
from utils.errors import InternalError, Conflict, NotFound
from utils.errors import request_error_handler
from utils.schema_validator import validate_schema
from validate_docbr import CPF

from api.DTO.registrationDTO import RegistrationDTO

import logging

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response
    from pymongo import MongoClient

VALIDATOR_SCHEMA_DICT = get_specification(schema_name="ValidatorRequest")


class Registration(BaseResource):
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    @request_error_handler
    def on_get_with_social_security_number(
        self, req: Request, res: Response, social_security_number: str = None
    ) -> NoReturn:

        # Mongo Collection
        logging.debug("Selecting MongoDB collection")
        db = self.mongo_client.registration_validator
        collection = db.registration

        # Searching for Registration
        logging.debug("Searching for registration")
        registration = collection.find_one(
            {"social_security_number": social_security_number}
        )

        # Raise exception if not found
        if not registration:
            logging.debug(
                f"Registration not found "
                f"(social_security_number: {social_security_number})"
            )
            raise NotFound(
                "No Registration found fot the given social_security_number"
            ).http()

        # Generate response
        logging.debug("Registration found, generating response")
        registration_dto = RegistrationDTO(db_object=registration)
        response = registration_dto.generate_response_body()
        self.generate_response(res=res, status_code=200, body_dict=response)

    @request_error_handler
    @falcon.before(action=validate_schema, schema_dict=VALIDATOR_SCHEMA_DICT)
    def on_post(self, req: Request, res: Response) -> NoReturn:
        body = req.media
        phone = body.get("phone")
        social_security_number = body.get("social_security_number")

        # Mongo Collection
        logging.debug("Selecting MongoDB collection")
        db = self.mongo_client.registration_validator
        collection = db.registration

        # Searching for Registration
        logging.debug("Searching for duplicate registration")
        registration = collection.find_one(
            {"social_security_number": social_security_number}
        )
        if registration:
            logging.debug(
                f"Duplicate registration found "
                f"(social_security_number: {social_security_number})"
            )
            raise Conflict(
                description=f"Registration already exists (social_security_number: {social_security_number})"
            ).http()

        # Validations
        logging.debug("Validating sent data")
        phone_validation = self.__validate_phone(phone=phone)
        social_security_number_validation = self.__validate_social_security_number(
            social_security_number=social_security_number
        )

        success = phone_validation and social_security_number_validation
        body["success"] = success

        # Generating response
        if success:
            logging.debug("The sent data is valid")
            registration_dto = RegistrationDTO(db_object=body)
            response = registration_dto.generate_response_body()
            self.generate_response(res=res, status_code=200, body_dict=response)
        else:
            logging.debug("The sent data is not valid")
            msg = self.__generate_error_msg(
                phone_validation=phone_validation,
                social_security_number_validation=social_security_number_validation,
            )
            body["msg"] = msg
            response_body = {"success": success, "msg": msg}
            self.generate_response(res=res, status_code=400, body_dict=response_body)

        # Save to database
        logging.debug(f"Saving new registration on MongoDB: {str(body)}")
        collection.insert_one(body)

    @staticmethod
    def __validate_phone(phone: str) -> bool:
        logging.debug("Validating phone")
        regex_pattern = "^\([1-9]{2}\)(?:[2-8]|9[1-9])[0-9]{7}$"  # noqa: W605
        match = re.fullmatch(pattern=regex_pattern, string=phone)
        logging.debug(f"Valid phone: {match}")
        return bool(match)

    @staticmethod
    def __validate_social_security_number(social_security_number: str) -> bool:
        logging.debug("Validating phone")
        cpf = CPF()
        valid_social_security_number = cpf.validate(doc=social_security_number)
        logging.debug(f"Valid social_security_number: {valid_social_security_number}")
        return valid_social_security_number

    @staticmethod
    def __generate_error_msg(
        phone_validation: bool, social_security_number_validation: bool
    ) -> str:
        logging.debug("Getting correct return message")
        msg_dict = {
            (False, False): "Invalid social_security_number and phone",
            (False, True): "Invalid  phone",
            (True, False): "Invalid social_security_number",
        }
        validation_tuple = (phone_validation, social_security_number_validation)
        return_msg = msg_dict.get(validation_tuple)
        if not return_msg:
            raise InternalError().http()
        logging.debug(f"Return message: {return_msg}")
        return return_msg
