from scrapy import cmdline
from lib.Log import Log

Log.clean()
cmdline.execute("scrapy crawl proxy".split())
