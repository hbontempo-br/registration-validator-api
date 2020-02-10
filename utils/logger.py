import logging
from typing import NoReturn

from constants import SERVICE_NAME

text_log_format = (
    "%(service_name)s :: "
    "%(levelname)s :: "
    "%(message)s :: "
    "%(pathname)s "
    "on method/function '%(funcName)s' "
    "(line %(lineno)s) "
    "at %(asctime)s "
    "(process: %(process)s "
    "[%(module)s] / "
    "request_track_id: %(request_track_id)s)"
)


class RequestTrack:
    request_track_id = None


class BaseLogger:
    def __init__(self, name: str = SERVICE_NAME, format: str = text_log_format):
        self.name = name
        self.format = format
        self.old_factory = logging.getLogRecordFactory()

    def config(self) -> NoReturn:
        logging.basicConfig(
            level=logging.DEBUG, format=text_log_format,
        )
        logging.setLogRecordFactory(self.__record_factory)

        logging.debug(msg="LogFormatter loaded")

    def __record_factory(self, *args, **kwargs) -> logging.LogRecord:
        record = self.old_factory(*args, **kwargs)
        record.service_name = self.name
        record.request_track_id = RequestTrack.request_track_id

        return record
