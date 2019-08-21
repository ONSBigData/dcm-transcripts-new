from common import *
from recordings.recording import *
import pandas as pd
import os


DIR = from_data_root('recordings/pyaudio_examples/')


def load_all():
    fnames = [
        f.replace('.wav', '')
        for f in os.listdir(DIR) if f.endswith('.wav')
    ]

    recordings = [load(fname) for fname in fnames]

    return recordings


def load(fname):
    r = Recording()

    r.audio_fpath = f'{DIR}/{fname}.wav'

    st_fpath = f'{DIR}/{fname}_st.csv'
    if not os.path.exists(st_fpath):
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

    df_st = pd.read_csv(st_fpath, index_col=0)
    r.structured_transcript = df_st

    r.no_speakers = df_st[COL_SPEAKER].nunique()

    return r


if __name__ == '__main__':
    print(load_all())
