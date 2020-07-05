# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from urllib.parse import urlparse
from urllib.request import proxy_bypass
from collections import defaultdict
from scrapy.utils.httpobj import urlparse_cached
import random


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MaoyanmovieSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaoyanmovieDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MaoyanmovieRandomProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.auth_encoding = auth_encoding
        self.proxies = defaultdict(list)
        for prxoy in proxy_list:
            parse = urlparse(prxoy)
            self.proxies[parse.scheme].append(prxoy)

    @classmethod
    def from_crawler(cls, crawler):
        # 此处因为猫眼电影是https协议，所以需要在settings.py里面的HTTP_PROXY_LIST使用https的代理ip
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured
        proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
        return cls(auth_encoding, proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        # request.headers["referer"] = 'https://maoyan.com/'
        # request.headers["cookie"] = '__mta=44439323.1593145138428.1593159946612.1593163905352.3; uuid_n_v=v1; uuid=23F8EC30B76411EAA2F937AFDFBC83F68905F9E8465D4E31AF7DFCAA143694B9; mojo-uuid=52400eb8e81e626cd376f2f156175e87; _lxsdk_cuid=172eed99c32c8-081bfffd57c6c9-3b634404-144000-172eed99c32c8; _lxsdk=23F8EC30B76411EAA2F937AFDFBC83F68905F9E8465D4E31AF7DFCAA143694B9; _csrf=490d6f65ecd2ff801739e69edb969097b564a9fd9a097d0da20247a541ac45ce; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593305661,1593929399,1593929418,1593929426; mojo-session-id={"id":"36c3c5c6e4e9f2179b8c88258749e340","time":1593938415434}; mojo-trace-id=6; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593940565; __mta=44439323.1593145138428.1593163905352.1593940565810.4; _lxsdk_s=1731e220f6d-616-9a8-581%7C%7C12'
        # print('=================使用的代理ip为：'+proxy)
