'''from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.spiders import Rule
import browsercookie

class MySpider(InitSpider):
    name = 'myspider'
    allowed_domains = ['washington.edu']
    login_page = 'http://weblogin.washington.edu/'
    start_urls = ['http://www.washington.edu/cec/toc.html']

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'name': 'jnv3', 'password': '*@Ja#9824147318!'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        print(response.body)
        self.initialized()

foo=MySpider()
url=foo.start_urls
cj=browsercookie.chrome()
req=Request(url[0], cookies=cj)
'''


import scrapy
import settings
from loginform import fill_login_form
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest

class MySpiderWithLogin(scrapy.Spider):
    name = 'my-spider'

    start_urls = [
        'http://www.washington.edu/cec/toc.html',
        'https://www.washington.edu/students/crscat/swa.html'
    ]

    login_url = 'http://weblogin.washington.edu/'

    login_user = 'jnv3'
    login_password = '*@Ja#9824147318!'
        
    def start_requests(self):
        # let's start by sending a first request to login page
        yield SplashRequest(self.login_url, self.parse_login, endpoint='render.json')

    def parse_login(self, response):
        # got the login page, let's fill the login form...
        data, url, method = fill_login_form(response.url, response.body,
                                            self.login_user, self.login_password)

        # ... and send a request with our login data
        return scrapy.FormRequest(url, formdata=dict(data),
                           method=method, callback=self.start_crawl)

    def start_crawl(self, response):
        # OK, we're in, let's start crawling the protected pages
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
            }, endpoint='render.json')

    def parse(self, response):
        # do stuff with the logged in response
        print('URL:',response.url)
        print('body:', response.text)

process = CrawlerProcess()

process.crawl(MySpiderWithLogin)
process.start()
