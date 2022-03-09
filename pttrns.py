from scrapy import cmdline
from lib.Log import Log

Log.clean()
# cmdline.execute(["scrapy", "crawl", "pttrns", "-o", "items.json"])
cmdline.execute("scrapy crawl pttrns".split())
