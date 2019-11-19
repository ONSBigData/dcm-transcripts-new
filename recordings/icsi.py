"""
From http://groups.inf.ed.ac.uk/ami/icsi/download/
"""

from common import *
from recordings.recording import *
import pandas as pd
import recordings.prep.segmenting_helper as sh

FPATH = from_data_root('recordings/icsi/')[:-1]
TRANSCRIPT_FPATH = f'{FPATH}/t'