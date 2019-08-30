"""
Based on http://www.voiptroubleshooter.com/open_speech
"""

from common import *
from recordings.recording import *
import recordings.prep.harvard.hv_common as hv_common
import recordings.prep.harvard.scrape_audio as scrape_audio
import recordings.prep.harvard.scrape_transcripts as scrape_transcripts
import recordings.prep.harvard.match_audio2transcripts as match_audio2tr
import pandas as pd
import os


def prep():
    print('This may take a while...')

    print('scraping audio files...')
    scrape_audio.scrape_audio()

    print('scraping transcripts...')
    scrape_transcripts.scrape_transcripts()

    print('mapping audios to their transcripts')
    match_audio2tr.create_matched_pairs()

    print('creating structured transcripts')
    prep_structured_transcripts()


def prep_structured_transcripts():
    for fname in get_fnames():
        st_fpath = f'{hv_common.DIR}/{fname}.txt'

        if os.path.exists(st_fpath):
            continue

        with open(st_fpath, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            st_fpath = f'{hv_common.DIR}/{fname}_struc_trancript.csv'

            df_st = pd.DataFrame(data=lines, columns=[COL_TEXT])
            df_st[COL_SPEAKER] = None
            df_st[COL_START] = None
            df_st[COL_END] = None
            df_st[COLS_STRUC_TRANSCRIPT].to_csv(st_fpath)


def get_fnames():
    return [
        f.replace('.wav', '')
        for f in os.listdir(hv_common.DIR) if f.endswith('.wav')
    ]


def load(fname):
    r = Recording()

    r.audio_fpath = f'{hv_common.DIR}/{fname}.wav'
    r.transcript_fpath = f'{hv_common.DIR}/{fname}.txt'

    r.no_speakers = 1

    st_fpath = f'{hv_common.DIR}/{fname}_struc_trancript.csv'
    df_st = pd.read_csv(st_fpath, index_col=0)
    r.pure_transcript = ' '.join(df_st[COL_TEXT])
    r.structured_transcript = df_st

    return r


def load_all():
    fnames = [
        f.replace('.wav', '')
        for f in os.listdir(hv_common.DIR) if f.endswith('.wav')
    ]

    recordings = [load(fname) for fname in fnames]

    return recordings


if __name__ == '__main__':
    # print(load_all())
    prep_structured_transcripts()
