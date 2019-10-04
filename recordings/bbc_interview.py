"""
Based on https://learnenglish.britishcouncil.org/advanced-c1-listening/job-interview
"""

from common import *
from recordings.recording import *
import pandas as pd
import recordings.prep.segmenting_helper as sh


FPATH = from_data_root('recordings/bbc_interview/')[:-1]
TRANSCRIPT_FPATH = f'{FPATH}/transcript.txt'
STRUC_TRANSCRIPT_FPATH = f'{FPATH}/struc_trancript.csv'


def prep():
    if os.path.exists(STRUC_TRANSCRIPT_FPATH):
        return

    df_st = sh.get_segmented_transcript(TRANSCRIPT_FPATH)
    df_st.to_csv(STRUC_TRANSCRIPT_FPATH)


def load():
    r = Recording()

    r.audio_fpath = f'{FPATH}/audio{DEF_AUDIO_SUFFIX}'
    r.transcript_fpath = TRANSCRIPT_FPATH

    r.no_speakers = 2

    df_st = pd.read_csv(STRUC_TRANSCRIPT_FPATH, index_col=0)
    r.pure_transcript = ' '.join(df_st[COL_TEXT])
    r.structured_transcript = df_st

    return r


if __name__ == '__main__':
    prep()
    print(load())
