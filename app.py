from api.adapters.sink import SinkAdapter
from api.resources.home import Home
import falcon
from middleware.input_output import InputOutputMiddleware
from middleware.request_track import RequestTrackMiddleware
from utils.logger import BaseLogger

BaseLogger().config()


def create() -> falcon.API:
    api = falcon.API(middleware=[RequestTrackMiddleware(), InputOutputMiddleware()])

    api.add_route(uri_template="/", resource=Home())

    api.add_sink(SinkAdapter(), r"/")

    return api


app = application = create()
