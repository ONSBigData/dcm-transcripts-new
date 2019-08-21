from common import *
import pandas as pd


def get_segmented_transcript(transcript_fpath):
    """
    Gets the segmented transcript from the text file where speakers
    are specified for each segment like this:

    Fero: bla bla bla

    Huw: bla bla bla
    """
    with open(transcript_fpath, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    segments = []
    segment = []
    for l in lines:
        if l.strip() == '':
            segment = ' '.join(segment)

            speaker = segment.split(':')[0]
            text = segment.split(':')[1]

            segments.append({
                COL_SPEAKER: speaker,
                COL_TEXT: text
            })

            segment = []
        else:
            segment.append(l)

    df_st = pd.DataFrame(data=segments)
    df_st[COL_START] = None
    df_st[COL_END] = None
    df_st = df_st[COLS_STRUC_TRANSCRIPT]

    return df_st
