import json

from lib.Log import Log
from pttrns.spiders.src.Image import Image
from scrapy import Spider, Request, FormRequest
from urllib.parse import urljoin


class Item:
    # def __init__(self, response):
    #     self.parse(response)

    start_urls = 'https://www.pttrns.com'

    def parse(self, response):

        if self.action(response) == 302:
            print(302)
            return
        page_url = response.url
        page_num = response.url.split("=")[-1]
        list = response.xpath('//div[@class="apps-collection w-dyn-items"]/*')
        for data in list:
            uri = data.xpath('./a/@href').extract()[0]
            small_name = uri.split("/")[-1]
            # item['icon'] = data.xpath('./a/div/img[1]/@src').extract()
            title = data.xpath('./a/div/div[1]/text()').extract()[0]
            if len(data.xpath('./a/div/div[2]/text()').extract()) > 0:
                description = data.xpath('./a/div/div[2]/text()').extract()[0]
            else:
                description = ''
            urls = urljoin(self.start_urls, uri)
            item = {'uri': page_url, 'title': title, 'description': description, 'page_num': page_num, 'small_name': small_name}
            yield Request(urls, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        if len(response.xpath('//div[@class="app-content-header-app"]/img/@src').extract()) > 0:
            item['icon'] = response.xpath('//div[@class="app-content-header-app"]/img/@src').extract()[0]
        else:
            item['icon'] = ''
        # item['image'] = response.xpath('//div[@class="patterns-collection w-dyn-items"]/*/div/a/img/@src').extract()
        item['app_category'] = response.xpath('//div[@class="app-content-header-app"]/div/div/div/div/div/text()').extract()
        images_uri = response.xpath('//div[@class="patterns-collection w-dyn-items"]/*/div/a/@href').extract()
        # yield item
        for image_uri in images_uri:
            image_urls = urljoin(self.start_urls, ''.join(image_uri))
            yield Request(image_urls, callback=self.parse_image, meta={"item": item})

    def parse_image(self, respon):
        item = respon.meta["item"]
        item['image_num'] = respon.url.split("/")[-1]
        item['image'] = respon.xpath('//div[@class="pattern-screenshot-bg"]/img/@src').extract()[0]
        image_tag = respon.xpath('//div[@class="pattern-info-metadata-block"][1]/div/div/div/a/text()').extract()
        # 图片的标签
        item['image_tag'] = list(set(image_tag).difference(set(item['app_category'])))
        # images
        images = []
        image_src_list = []
        tags = []
        if item['icon'] == '':
            icon_path = ''
        else:
            icon_img = {
                'img': item['icon'],
                'type': 'content_icon',
            }
            image_src_list.append(icon_img)
            if item['icon'] == "https://assets-global.website-files.com":
                icon_path = 'content_icon/' + item['small_name'] + '-not_icon' + '.jpg'
            else:
                icon_path = 'content_icon/' + item['small_name'] + '.jpg'

        if item['image'] == '':
            image_path = ''
        else:
            image_path = 'images/' + item['image_num'] + '.jpg'
            image_img = {
                'img': item['image'],
                'type': 'images',
            }
            # image_src_list.append(item['image'])
            image_src_list.append(image_img)
        tags.append({
            'title': item['title'],
            'tags': item['image_tag']
        })
        item_img = {
            'title': item['title'],
            'no': item['image_num'],
            'src': image_path,
            'tags': tags
        }
        images.append(item_img)
        Log.debug(item_img)
        page = {
            'no': item['image_num'],
            'uri': item['uri'],
            'icon': item['icon'],
            'icon_path': icon_path,
            'title': item['title'],
            'description': item['description'],
            'name_on': item['small_name'],
            'image': item['image'],
            'image_path': image_path,
            'images': images,
            'tags': {
                'tags': item['image_tag'],
                'categories': item['app_category'],

            }
        }
        imageItem = Image()
        imageItem['image_urls'] = image_src_list
        imageItem['no'] = item['image_num']
        imageItem['title'] = item['small_name']
        yield imageItem
        self.save(page)
        # Log.debug(imageItem.images)

    def filter(self, str):
        # str = str.replace("\\u", '')
        str = str.replace("\\n", '')
        return str.strip()

    def save(self, page):
        filename = './data/pages/page/' + page['no'] + '.json'
        with open(filename, 'w') as f:
            page = json.dumps(page, sort_keys=True, ensure_ascii=True, indent=2, separators=(',', ': '))
            f.write(page)

    def action(self, response):
        request = response.request
        if hasattr(request.meta, 'redirect_urls') and request.url != request.meta['redirect_urls'][0]:
            return 302

        return 200
