import scrapy
import scrapy.crawler as crawler
import twisted.internet.reactor as reactor
import urllib.request
import requests
import lxml.html as html
import pickle
from common import *


DIR = from_data_root(f'recordings/harvard/', create_if_needed=True)[:-1]
TRANSCRIPTS_FPATH = f'{DIR}/transcripts.pickle'


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
            filename = l[l.rindex('/') + 1:]
            filepath = f'{DIR}/{filename}'
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


def scrape_transcripts():
    url = 'http://www.cs.columbia.edu/~hgs/audio/harvard.html'

    response = requests.get(url)

    content = html.fromstring(response.content)
    lists = content.xpath('//ol')
    texts = [[text for text in l.xpath('li/text()')] for l in lists]

    with open(TRANSCRIPTS_FPATH, 'wb') as f:
        pickle.dump(texts, f)

    return texts


def load():
    with open(TRANSCRIPTS_FPATH, 'rb') as f:
        texts = pickle.load(f)

    return texts


if __name__ == '__main__':
    # scrape_transcripts()
    print(load())
