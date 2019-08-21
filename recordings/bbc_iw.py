from common import *
from recordings.recording import *
import pandas as pd
import os
import recordings.prep.segmenting_helper as sh


def load():
    r = Recording()

    fpath = from_data_root('recordings/bbc-interview/')

    r.audio_fpath = f'{fpath}/audio.wav'
    r.transcript_fpath = f'{fpath}/transcript.txt'

    r.no_speakers = 2

    st_fpath = f'{fpath}/st.csv'
    if not os.path.exists(st_fpath):
        df_st = sh.get_segmented_transcript(r.transcript_fpath)
        df_st.to_csv(st_fpath)

    df_st = pd.read_csv(st_fpath, index_col=0)
    r.pure_transcript = ' '.join(df_st[COL_TEXT])
    r.structured_transcript = df_st

    return r


if __name__ == '__main__':
    print(load())
