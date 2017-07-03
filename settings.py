'''
    Basic splash config.
'''

# splash server address
SPLASH_URL = 'http://192.168.59.103:8050'

# enable the splash middleware and changing the HttpCompressionMiddleware priority
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enabling SplashDeduplicateArgsMiddleware
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Set a custom dupefilter class
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# Scrapy custom cache 
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
