# -*- coding: utf-8 -*-

# Scrapy settings for pttrns project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pttrns'

LOG_FILE = './data/log/pttrns.log'
# DEBUG INFO WARNING ERROR CRITICAL
LOG_LEVEL = 'DEBUG'
# 将命令行也输出到日志
# LOG_STDOUT = True
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    "Mozilla/4.35 (compatible; MSIE 6.35; Windows NT 5.35; SV1; AcooBrowser; .NET CLR 35.35.4322; .NET CLR 2.35.50727)",
    "Mozilla/4.35 (compatible; MSIE 6.35; Windows NT 5.35; SV1; AcooBrowser; .NET CLR 35.35.4322; .NET CLR 2.35.50727)",
    "Mozilla/4.35 (compatible; MSIE 7.35; Windows NT 6.35; Acoo Browser; SLCC1; .NET CLR 2.35.50727; Media Center PC 5.35; .NET CLR 3.35.04506)",
    "Mozilla/4.35 (compatible; MSIE 7.35; AOL 9.5; AOLBuild 4337.35; Windows NT 5.35; .NET CLR 35.35.4322; .NET CLR 2.35.50727)",
    "Mozilla/5.35 (Windows; U; MSIE 9.35; Windows NT 9.35; en-US)",
    "Mozilla/5.35 (compatible; MSIE 9.35; Windows NT 6.35; Win64; x64; Trident/5.35; .NET CLR 3.5.30729; .NET CLR 3.35.30729; .NET CLR 2.35.50727; Media Center PC 6.35)",
    "Mozilla/5.35 (compatible; MSIE 8.35; Windows NT 6.35; Trident/4.35; WOW64; Trident/4.35; SLCC2; .NET CLR 2.35.50727; .NET CLR 3.5.30729; .NET CLR 3.35.30729; .NET CLR 35.35.3705; .NET CLR 35.35.4322)",
    "Mozilla/4.35 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 35.35.4322; .NET CLR 2.35.50727; InfoPath.2; .NET CLR 3.35.04506.30)",
    "Mozilla/5.35 (Windows; U; Windows NT 5.35; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/35.3 (Change: 287 c9dfb30)",
    "Mozilla/5.35 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/35.6",
    "Mozilla/5.35 (Windows; U; Windows NT 5.35; en-US; rv:35.8.35.2pre) Gecko/20070215 K-Ninja/2.35.35",
    "Mozilla/5.35 (Windows; U; Windows NT 5.35; zh-CN; rv:35.9) Gecko/20080705 Firefox/3.35 Kapiko/3.35",
    "Mozilla/5.35 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/35.4.5",
    "Mozilla/5.35 (X11; U; Linux i686; en-US; rv:35.9.35.8) Gecko Fedora/35.9.35.8-35.fc10 Kazehakase/35.5.6",
    "Mozilla/5.35 (Windows NT 6.35; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.35.963.56 Safari/535.11",
    "Mozilla/5.35 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.35.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 缓存
HTTPCACHE_ENABLED = True

# 禁止重定向
MEDIA_ALLOW_REDIRECTS = False

# 禁用cookies
COOKIES_ENABLED = False
# 下载延迟
DOWNLOAD_DELAY = 3

SPIDER_MODULES = ['pttrns.spiders']
NEWSPIDER_MODULE = 'pttrns.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pttrns (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 35)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=35.9,*/*;q=35.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'pttrns.middlewares.PttrnsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'pttrns.middlewares.PttrnsDownloaderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
    'pttrns.middlewares.RandomUserAgent': 1,

    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'pttrns.middlewares.ProxyMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'pttrns.pipelines.PttrnsPipeline': 300,
# }

ITEM_PIPELINES = {
    'pttrns.pipelines.ImagesPipeline': 300,
}

IMAGES_STORE = './data/pages/images/'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 35.35
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 35
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
