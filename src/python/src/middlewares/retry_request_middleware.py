from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy import Request
from scrapy.http import Response
from twisted.internet.defer import Deferred
from scrapy.utils.response import response_status_message
from scrapy.utils.misc import load_object
from scrapy.exceptions import NotConfigured


class RetryRequestMiddleware(RetryMiddleware):
    custom_setting = {
        "RETRY_ENABLED": True,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 522, 524, 408, 429, 403]
    }

    def __init__(self, settings):
        settings = {**settings, **self.custom_setting}
        if not settings.get("RETRY_ENABLED"):
            raise NotConfigured
        self.max_retry_times = settings.get("RETRY_TIMES")
        self.retry_http_codes = set(
            int(x) for x in settings.get("RETRY_HTTP_CODES")
        )
        self.priority_adjust = settings.get("RETRY_PRIORITY_ADJUST")
        try:
            self.exceptions_to_retry = self.__getattribute__("EXCEPTIONS_TO_RETRY")
        except AttributeError:
            # If EXCEPTIONS_TO_RETRY is not "overridden"
            self.exceptions_to_retry = tuple(
                load_object(x) if isinstance(x, str) else x
                for x in settings.get("RETRY_EXCEPTIONS")
            )

