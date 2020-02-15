from api.DTO.base_DTO import BaseDTO


class RegistrationDTO(BaseDTO):
    def __init__(self, db_object: dict):
        super().__init__(db_object=db_object)
