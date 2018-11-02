# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
from selenium import webdriver
import scrapy


class SeleniumMiddlerware(object):
    def process_request(self,request,spider):
        # if request.url == 'http://data.eastmoney.com/zjlx/list.html':
        self.web_driver = webdriver.ChromeOptions()
        self.web_driver.add_argument('--headless')
        self.web_driver.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=self.web_driver)
        self.driver.get(request.url)
        time.sleep(2)
        html = self.driver.page_source
        self.driver.quit()
        response = scrapy.http.HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
        return response

class TreasureDownloaderMiddleware(object):
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
