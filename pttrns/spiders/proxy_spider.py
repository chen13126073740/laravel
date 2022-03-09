import scrapy
import json


class proxy(scrapy.Spider):
    name = "proxy"
    list = []
    page = 2

    def start_requests(self):
        url = "http://www.xicidaili.com/wt/"
        # 1888
        for i in range(1, self.page + 1):
            yield scrapy.Request(url=url + str(i), callback=self.parse)

    def parse(self, response):

        trs = response.css('table#ip_list .odd')
        for tr in trs:
            tds = tr.css('td::text').extract()
            ip = tds[0]
            port = tds[1]
            delay = float(tr.css('td div::attr(title)').extract()[0].replace('秒', ''))
            if delay > 1:
                continue

            print(delay)
            item = {
                'ip': ip,
                'port': port,
                'delay': str(delay)
            }
            self.list.append(item)

        page = int(response.url.split("/")[-1])
        if page == self.page:
            myfile = open('./data/proxy/35.json', 'w')
            json.dump(self.list, myfile, indent=4)
            myfile.close()
