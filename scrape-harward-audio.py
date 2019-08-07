import scrapy
import scrapy.crawler as crawler
import twisted.internet.reactor as reactor
import urllib.request
from common import *


class HarvardAudioSpider(scrapy.Spider):
    name = "harvard-audio"

    def start_requests(self):
        urls = [
            'http://www.voiptroubleshooter.com/open_speech/british.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fromurl = response.url[:response.url.rindex('/')]
        links = response.xpath("//table[@bordercolor='#C0C0C0']")[0].xpath('.//a/@href').extract()
        for l in links:
            filename = l[l.rindex('/') + 1:]
            filepath = from_data_root(f'recordings/harvard/{filename}', create_if_needed=True)
            urllib.request.urlretrieve(f'{fromurl}/{l}', filename)

settings = {
    'LOG_ENABLED': False,
    'BOT_NAME': 'test_spider',
    'ROBOTSTXT_OBEY': True
}

runner = crawler.CrawlerRunner(settings)
deferred = runner.crawl(HarvardAudioSpider)


def _cb():
    reactor.stop()


deferred.addBoth(lambda _: _cb())

reactor.run()
