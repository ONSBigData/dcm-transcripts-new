"""
Taken from https://github.com/tyiannak/pyAudioAnalysis/tree/master/pyAudioAnalysis/data
"""

from common import *
from recordings.recording import *
import pandas as pd
import os


DIR = from_data_root('recordings/pyaudio_examples/')[:-1]


def get_fnames():
    return [
        f.replace('.mp3', '')
        for f in os.listdir(DIR) if f.endswith('.mp3')
    ]


def prep():
    for fname in get_fnames():
        st_fpath = f'{DIR}/{fname}_struc_trancript.csv'
        if os.path.exists(st_fpath):
            continue

        with open(f'{DIR}/{fname}.segments', 'r') as f:
            lines = [l for l in f.readlines() if l.strip() != '']
            segments = [{
                COL_START: l.split(',')[0],
                COL_END: l.split(',')[1],
                COL_SPEAKER: l.split(',')[2].strip(),
            } for l in lines]
            df_st = pd.DataFrame(data=segments)
            df_st[COL_TEXT] = None
            df_st.to_csv(st_fpath)


def load_all():
    return [load(fname) for fname in get_fnames()]


def load(fname):
    r = Recording()

    r.audio_fpath = f'{DIR}/{fname}.mp3'

    df_st = pd.read_csv(f'{DIR}/{fname}_struc_trancript.csv', index_col=0)
    r.structured_transcript = df_st

    r.no_speakers = df_st[COL_SPEAKER].nunique()

    return r


if __name__ == '__main__':
    prep()
    print(load_all())
