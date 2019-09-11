"""
Taken from https://github.com/tyiannak/pyAudioAnalysis/tree/master/pyAudioAnalysis/data
"""

from common import *
from recordings.recording import *
import pandas as pd
import os


DIR = from_data_root('recordings/dcm_test_iws/')[:-1]


def get_fnames():
    return [
        f.replace(DEF_AUDIO_SUFFIX, '')
        for f in os.listdir(DIR) if f.endswith(DEF_AUDIO_SUFFIX)
    ]


def prep():
    pass # nothing so far


def load_all():
    return [load(fname) for fname in get_fnames()]


def load(fname):
    r = Recording()

    r.audio_fpath = f'{DIR}/{fname}{DEF_AUDIO_SUFFIX}'

    r.structured_transcript = None
    r.no_speakers = None

    return r


if __name__ == '__main__':
    prep()
    print(load_all())
