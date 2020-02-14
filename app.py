from api.adapters.sink import SinkAdapter
from api.resources.home import Home
from api.resources.validator import Validator
import falcon
from middleware.input_output import InputOutputMiddleware
from middleware.request_track import RequestTrackMiddleware
from utils.logger import BaseLogger

BaseLogger().config()


def create() -> falcon.API:
    api = falcon.API(middleware=[RequestTrackMiddleware(), InputOutputMiddleware()])

    api.add_route(uri_template="/", resource=Home())

    validator = Validator()
    api.add_route(uri_template="/validator", resource=validator)
    api.add_route(
        uri_template="/validator/{social_security_number}",
        resource=validator,
        suffix="with_social_security_number",
    )

    api.add_sink(SinkAdapter(), r"/")

    return api


app = application = create()
