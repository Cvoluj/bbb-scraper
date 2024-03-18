import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware, get_retry_request
from scrapy import Request
from scrapy.utils.misc import load_object
from scrapy.exceptions import NotConfigured
from middlewares import HttpProxyMiddleware


class RetryRequestMiddleware(RetryMiddleware):
    custom_setting = {
        "RETRY_ENABLED": True,
        "RETRY_HTTP_CODES": [502, 503, 504, 522, 524, 408, 429, 403],
        "RETRY_TIMES": 5
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
            self.exceptions_to_retry = tuple(
                load_object(x) if isinstance(x, str) else x
                for x in settings.get("RETRY_EXCEPTIONS")
            )

    def _retry(self, request: Request, reason, spider):
        if reason != '403 Forbidden':
            return super()._retry(request, reason, spider)
        
        request.headers["Connection"] = "close"
        try:
            return get_retry_request(request=request, 
                                 spider=spider, 
                                 max_retry_times=self.max_retry_times, 
                                 priority_adjust=self.priority_adjust) 
        except:
            logging.warning('Empty url')
