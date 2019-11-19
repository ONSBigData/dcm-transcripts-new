"""
From http://groups.inf.ed.ac.uk/ami/icsi/download/
"""

from common import *
from recordings.recording import *
import pandas as pd
import os


DIR = from_data_root('recordings/icsi')


def get_fnames():
    return [
        f.replace('.wav', '')
        for f in os.listdir(DIR) if f.endswith('.wav')
    ]


def prep():
    pass


def load_all():
    return [load(fname) for fname in get_fnames()]


def load(fname):
    r = Recording()

    r.audio_fpath = f'{DIR}/{fname}.wav'

    r.structured_transcript = None
    r.no_speakers = None

    return r


if __name__ == '__main__':
    prep()
    print(load_all())