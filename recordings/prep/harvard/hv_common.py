from common import *


DIR = from_data_root(f'recordings/harvard/', create_if_needed=True)[:-1]

DIR_MATCHED = from_data_root(
    f'recordings/harvard/matched/',
    create_if_needed=True
)[:-1]

MAPPING_FPATH = f'{DIR}/mapping.csv'
