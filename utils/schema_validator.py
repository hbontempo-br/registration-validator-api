from __future__ import annotations

import json
from typing import Dict
from typing import TYPE_CHECKING

import jsonschema
from utils.errors import BadRequest

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response
    from api.resources.base_resource import BaseResource


def validate_schema(
    req: Request,
    resp: Response,
    resource: BaseResource,
    params: Dict,
    schema_dict: Dict,
):

    validator = jsonschema.Draft7Validator(schema_dict)
    error_generator = validator.iter_errors(req.media)
    errors = [str(error) for error in error_generator]
    if errors:
        raise BadRequest(description=json.dumps(errors)).http()
