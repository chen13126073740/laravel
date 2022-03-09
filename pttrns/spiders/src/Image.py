import scrapy


class Image(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    no = scrapy.Field()
    title = scrapy.Field()
