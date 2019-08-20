from common import *
import recordings.prep.harvard.hv_common as hv_common


def load_all():
    fnames = [f for f in os.listdir(hv_common.DIR) if f.endswith('.wav')]


    with open(TRANSCRIPTS_FPATH, 'rb') as f:
        texts = pickle.load(f)


    uk_wavs  = [f for f in wavs if '_uk_' in f]
    us_wavs = [f for f in wavs if '_us_' in f]

    return {
        'transcripts': texts,
        'audio': {
            'uk': uk_wavs,
            'us': us_wavs
        }
    }


if __name__ == '__main__':
    scrape_audio()
