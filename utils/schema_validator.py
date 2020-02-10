from __future__ import annotations

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
    try:
        jsonschema.validate(
            req.media, schema_dict, format_checker=jsonschema.FormatChecker(),
        )
    except jsonschema.ValidationError as e:
        raise BadRequest(description=e.message).http()
