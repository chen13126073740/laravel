import scrapy

from pttrns.spiders.src.Item import Item
from lib.Log import Log
from scrapy import Spider, Request, FormRequest


class pttrns(scrapy.Spider):
    name = "pttrns"
    max_page = 7  # 78

    def start_requests(self):
        item = Item()
        url = 'https://www.pttrns.com/apps?62f5231c_page='
        for i in range(1, self.max_page + 1):
            Log.debug('start')
            print(i)
            yield scrapy.Request(url=url + str(i), callback=item.parse)
