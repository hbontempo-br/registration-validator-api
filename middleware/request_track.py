from __future__ import annotations

import logging
from typing import NoReturn
from typing import TYPE_CHECKING
import uuid

from utils.logger import RequestTrack

if TYPE_CHECKING:
    from falcon import Request, Response
    from api.resources.base_resource import BaseResource


class RequestTrackMiddleware:
    def process_request(self, req: Request, res: Response) -> NoReturn:
        new_request_track_id = req.get_header("request-track-id")
        if new_request_track_id:
            RequestTrack.request_track_id = new_request_track_id
        else:
            RequestTrack.request_track_id = str(uuid.uuid4())
        logging.debug("Request Track ID loaded")

    def process_response(
        self, req: Request, res: Response, resource: BaseResource, req_succeeded: bool
    ) -> NoReturn:
        res.set_headers(headers={"request-track-id": RequestTrack.request_track_id})
        self.__clear_tracking_ids()

    def __clear_tracking_ids(self) -> NoReturn:
        RequestTrack.request_track_id = None
