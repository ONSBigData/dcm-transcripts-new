import requests
import lxml.html as html
import recordings.prep.harvard.hv_common as hv_common


def scrape_transcripts():
    url = 'http://www.cs.columbia.edu/~hgs/audio/harvard.html'

    response = requests.get(url)

    content = html.fromstring(response.content)
    lists = content.xpath('//ol')
    texts = [[text for text in l.xpath('li/text()')] for l in lists]

    for i, t in enumerate(texts):
        with open(f'{hv_common.DIR_PREP}/transcript_{i}.txt', 'w') as f:
            f.writelines([l + '\n' for l in t])

    return texts


if __name__ == '__main__':
    scrape_transcripts()
