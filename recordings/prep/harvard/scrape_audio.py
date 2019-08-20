import scrapy
import scrapy.crawler as crawler
import twisted.internet.reactor as reactor
import urllib.request
import recordings.prep.harvard.hv_common as harvard_common
from common import *


class HarvardAudioSpider(scrapy.Spider):
    name = "harvard-audio"

    def start_requests(self):
        urls = [
            'http://www.voiptroubleshooter.com/open_speech/british.html',
            'http://www.voiptroubleshooter.com/open_speech/american.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        fromurl = response.url[:response.url.rindex('/')]
        links = response.xpath("//table[@bordercolor='#C0C0C0']")[0].xpath('.//a/@href').extract()
        for l in links:
            if 'OSR_us_000_0058_8k.wav' in l:
                # this one is broken audio file
                continue
            filename = l[l.rindex('/') + 1:]
            filepath = f'{harvard_common.DIR}/{filename}'
            print(f'Downloading {l} to {filepath}')
            urllib.request.urlretrieve(f'{fromurl}/{l}', filepath)


def scrape_audio():
    settings = {
        'LOG_ENABLED': False,
        'BOT_NAME': 'test_spider',
        'ROBOTSTXT_OBEY': True
    }

    runner = crawler.CrawlerRunner(settings)
    deferred = runner.crawl(HarvardAudioSpider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    scrape_audio()
