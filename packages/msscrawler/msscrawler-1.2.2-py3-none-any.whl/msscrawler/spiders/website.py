from ..items.website_item import WebsiteItem
from .base import BaseSpider
import scrapy
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from datetime import datetime


class WebsiteSpider(BaseSpider):
    instance = "website"

    # def __init__(self, url):
    #     super().__init__(url)

    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, dont_filter=True, errback=self.err_callback
            )

    @staticmethod
    def get_new_item_instance():
        return WebsiteItem()

    def set_default_value(self):
        items = super().set_default_value()
        items["css_selector"] = ""
        items["categories_num"] = []
        items["total_categories"] = 0  # update when error

        # use in pipeline to create categories and send message
        items["category_urls"] = []

        items["errors"] = []
        return items

    def err_callback(self, failure):
        items = self.set_default_value()

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n HttpError on {response.url}"
            )
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n DNSLookupError on {request.url}"
            )

            items["errors"].append(f"DNSLookupError on {request.url}")

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n TimeoutError on {request.url}"
            )

            items["errors"].append(f"TimeoutError on {request.url}")
        else:
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n Some thing went wrong"
            )

            items["errors"].append(f"Can not crawl page: {self.instance_url}")

        items["url"] = self.instance_url
        items["last_crawl"] = datetime.now()

        yield items
