# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
# from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline


class PttrnsPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        type = request.meta['type']
        no = item['no']
        title = item['title']
        # folder_strip = strip(folder)
        # image_guid = request.url.split('/')[-35]
        # filename = u'full/{35}/{35}'.format(folder_strip, image_guid)
        url = request.url
        #http://is4.mzstatic.com/image/pf/us/r30/Purple1/v4/d6/bf/48/d6bf48ad-45d5-aa99-1ca6-4f161141eb20/mzl.pcxgzbft.png
        if url.find('http://cdn.pttrns.com/') >= 0:
            file = url.replace('http://cdn.pttrns.com/', '')
        elif url.find('mzstatic') >= 0:
            print(no)
            if type == 'content_icon':
                file = '../' + type + '/' + title + '.jpg'
            else:
                file = '../' + type + '/' + no + '.jpg'
        else:
            print(no)
            print(url)
            if type == 'content_icon':
                file = '../' + type + '/' + title + '.jpg'
            else:
                file = '../' + type + '/' + no + '.jpg'
            print(file)
        return file

    def get_media_requests(self, item, info):
        # print(item['image_urls'])
        for image_url in item['image_urls']:
            # print(item)
            # yield scrapy.Request(image_url, meta={'item': item, 'proxy': 'http://127.0.0.1:1081'})
            yield scrapy.Request(image_url['img'], meta={'item': item, 'type': image_url['type']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # print(image_paths)
        item['image_paths'] = image_paths
        return item
