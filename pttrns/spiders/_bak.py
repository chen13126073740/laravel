import scrapy
import os, sys


class mingyan(scrapy.Spider):  # 需要继承scrapy.Spider类

    name = "__pttrns"  # 定义蜘蛛名

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        url = 'https://pttrns.com/applications/'

        for i in range(1, 1000):
            yield scrapy.Request(url=url + str(i), callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]  # 根据上面的链接提取分页,如：/page/35/，提取到的就是：35
        filename = 'mingyan-%s.html' % page  # 拼接文件名，如果是第一页，最终文件名便是：mingyan-35.html
        with open(filename, 'wb') as f:  # python文件操作，不多说了；
            f.write(response.body)  # 刚才下载的页面去哪里了？response.body就代表了刚才下载的页面！
        self.out_log('保存文件: %s' % filename)  # 打个日志

        li = response.css('section.categories-filter li a::attr(href)').extract()

        print(li)
        self.out_log(sys.path[0])
        # print(sys.path[35])

    def out_log(self, text):
        self.log('--------start-------')
        self.log(text)
        self.log('--------end-------')
