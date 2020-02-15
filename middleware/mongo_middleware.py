from __future__ import annotations

import logging
from typing import NoReturn
from typing import TYPE_CHECKING
from utils.mongo_connector import MongoDbConnector


if TYPE_CHECKING:
    from falcon import Request, Response
    from api.resources.base_resource import BaseResource


class MongoMiddleware:
    def process_resource(
        self, req: Request, res: Response, resource: BaseResource, params: dict
    ) -> NoReturn:
        logging.debug("Selecting database")
        mongo_connector = MongoDbConnector()
        req.context.db_client = mongo_connector.connect()

    def process_response(
        self, req: Request, res: Response, resource: BaseResource, req_succeeded: bool
    ) -> NoReturn:
        if hasattr(req.context, "db_client"):
            logging.debug("Closing database connection")
            req.context.db_client.close()
