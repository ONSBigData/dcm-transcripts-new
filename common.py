"""
Most commonly used methods/constants, used across the whole project
"""

import os
import time
import logging

# ---------------------------------------------------------------------
# --- Config
# ---------------------------------------------------------------------

ROOT_FOLDER = '/../'  # set where is the root folder of this project, relative of this file
SRC_FOLDER = '/'  # set where is the source root folder of this project, relative of this file
DATA_FOLDER = '/../data/'  # set where is the data folder (storing e.g. outputs from scraping), relative of this file

DEF_AUDIO_SUFFIX = '.mp3'


# ---------------------------------------------------------------------
# --- Constants
# ---------------------------------------------------------------------

COL_SPEAKER = 'speaker'
COL_START = 'from'
COL_END = 'end'
COL_TEXT = 'text'
COLS_STRUC_TRANSCRIPT = [COL_SPEAKER, COL_START, COL_END, COL_TEXT]


# ---------------------------------------------------------------------
# --- Commonly used functions
# ---------------------------------------------------------------------


def path2id(audio_fpath, level_from=-2, level_to=None):
    """
    E.g. from

    "/home/ons21553/wspace/interview-transcripts/data/recordings/bbc_interview/audio.mp3"

    makes

    "bbc_interview__audio"
    """

    audio_fpath = os.path.abspath(audio_fpath)

    _id = '.'.join(audio_fpath.split('.')[:-1])
    _id = '__'.join(_id.split('/')[level_from:level_to])

    return _id


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(asctime)s: %(message)s'
    )


def create_directories_if_necessary(path):
    """
    Given a path, creates all the directories necessary till the last '/' encountered. E.g.

    if '/path/to/' exists and the path argument is '/path/to/file/is/this',
    calling this would create '/path/to/file/is/'
    """

    if '/' not in path:
        return

    dir_path = path[0:path.rfind('/') + 1]

    if os.path.exists(dir_path):
        return

    os.makedirs(dir_path)


def from_root(path, create_if_needed=False):
    """
    Returns path with project root prepended
    """
    proj_root = os.path.realpath(os.path.dirname(__file__)) + ROOT_FOLDER
    result_path = proj_root + path

    if create_if_needed:
        create_directories_if_necessary(result_path)

    return result_path


def from_src_root(path, create_if_needed=False):
    """
    Returns path with project root prepended
    """
    return from_root(f'src/{path}', create_if_needed=create_if_needed)


def from_data_root(path, create_if_needed=False):
    """
    Returns path with data project root prepended
    """
    proj_data_root = os.path.realpath(os.path.dirname(__file__)) + DATA_FOLDER
    result_path = proj_data_root + path

    if create_if_needed:
        create_directories_if_necessary(result_path)

    return result_path

# ---------------------------------------------------------------------
# --- Timing of code
# ---------------------------------------------------------------------


__start_times = {}


def start_timing(id, msg=''):
    __start_times[id] = time.time()

    print()
    print('v'*20)
    print(f'START of timing {id}: {msg}')


def end_timing(id, msg=''):
    start_time = __start_times[id]
    duration = time.time() - start_time
    minutes = int(duration // 60)
    secs = duration % 60

    print(f'END of timing {id}: {msg} ({minutes}m, {secs:.1f}s)')
    print('^'*20)
    print()


