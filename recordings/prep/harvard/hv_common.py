from common import *


DIR = from_data_root(f'recordings/harvard/', create_if_needed=True)[:-1]

DIR_PREP = from_data_root(
    f'recordings/harvard/prep/',
    create_if_needed=True
)[:-1]


MAPPING_FPATH = f'{DIR_PREP}/mapping.csv'
