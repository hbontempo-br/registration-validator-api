from utils.logger import BaseLogger

# Logger is started here because it needs to run before packages have their own logging
# configuration and invalidates this customization
BaseLogger().config()

from api.adapters.sink import SinkAdapter  # noqa: E402
from api.resources.home import Home  # noqa: E402
from api.resources.registration import Registration  # noqa: E402
import falcon  # noqa: E402
from middleware.input_output import InputOutputMiddleware  # noqa: E402
from middleware.request_track import RequestTrackMiddleware  # noqa: E402
from middleware.mongo_middleware import MongoMiddleware  # noqa: E402


def create() -> falcon.API:
    api = falcon.API(
        middleware=[
            RequestTrackMiddleware(),
            InputOutputMiddleware(),
            MongoMiddleware(),
        ]
    )

    api.add_route(uri_template="/", resource=Home())

    validator = Registration()
    api.add_route(uri_template="/registration", resource=validator)
    api.add_route(
        uri_template="/registration/{social_security_number}",
        resource=validator,
        suffix="with_social_security_number",
    )

    api.add_sink(SinkAdapter(), r"/")

    return api


app = application = create()
