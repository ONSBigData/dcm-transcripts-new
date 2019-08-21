from common import *
from recordings.recording import *
import recordings.prep.harvard.hv_common as hv_common
import pandas as pd
import os


def load(fname):
    r = Recording()

    r.audio_fpath = f'{hv_common.DIR_MATCHED}/{fname}.wav'
    r.transcript_fpath = f'{hv_common.DIR_MATCHED}/{fname}.txt'

    r.no_speakers = 1

    with open(r.transcript_fpath, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        r.pure_transcript = ' '.join(lines)

        st_fpath = f'{hv_common.DIR_MATCHED}/{fname}_st.csv'
        if not os.path.exists(st_fpath):
            df_st = pd.DataFrame(data=lines, columns=[COL_TEXT])
            df_st[COL_SPEAKER] = None
            df_st[COL_START] = None
            df_st[COL_END] = None
            df_st[COLS_STRUC_TRANSCRIPT].to_csv(st_fpath)

        r.structured_transcript = pd.read_csv(st_fpath, index_col=0)

    return r


def load_all():
    fnames = [
        f.replace('.wav', '')
        for f in os.listdir(hv_common.DIR_MATCHED) if f.endswith('.wav')
    ]

    recordings = [load(fname) for fname in fnames]

    return recordings


if __name__ == '__main__':
    print(load_all())
