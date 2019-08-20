from common import *
from editdist import levenshtein
import speech_recognition as sr
import recordings.prep.harvard.hv_common as hv_common
import pandas as pd
import shutil
import re


def find_transcript(audio_fpath, all_transcripts):
    recognizer = sr.Recognizer()

    print(f'\nfinding the best transcript for {audio_fpath}')
    with sr.AudioFile(audio_fpath) as source:
        audio = recognizer.record(source)

    recog_text = recognizer.recognize_google(audio)

    scores = [{
        'transcript_fpath': fpath,
        'text': text,
        'distance': levenshtein(recog_text, text)
    } for fpath, text in all_transcripts.items()]

    scores.sort(key=lambda score: score['distance'])

    result = {
        'audio_fpath': audio_fpath,
        **scores[0],
        'next_distance': scores[1]['distance']
    }

    print(f'found {result}')

    return result


def make_mappings():
    text_fpaths = [f'{hv_common.DIR}/{f}' for f in os.listdir(hv_common.DIR) if re.search(r'transcript_\d.txt', f)]

    all_transcripts = {}
    for fpath in text_fpaths:
        with open(fpath, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            all_transcripts[fpath] = ' '.join(lines)

    audio_fpaths = [f'{hv_common.DIR}/{f}' for f in os.listdir(hv_common.DIR) if f.endswith('.wav')]

    results = [find_transcript(audio_fpath, all_transcripts) for audio_fpath in audio_fpaths]

    # only if there's one transcript significantly better than others we will take it as the correct one
    THRESHOLD = 1.7
    mapping = {
        r['audio_fpath']: (r['transcript_fpath'] if r['distance']*THRESHOLD < r['next_distance'] else None)
        for r in results
    }

    pd.Series(mapping).to_csv(hv_common.MAPPING_FPATH)


def create_matched_pairs():
    mapping = pd.read_csv(hv_common.MAPPING_FPATH, header=None, names=['audio_fpath', 'transcript_fpath'])
    for r in mapping.dropna().iterrows():
        fname = os.path.basename(r[1]['audio_fpath']).replace('.wav', '')
        shutil.copyfile(r[1]['audio_fpath'], f'{hv_common.DIR_MATCHED}/{fname}.wav')
        shutil.copyfile(r[1]['transcript_fpath'], f'{hv_common.DIR_MATCHED}/{fname}.txt')


if __name__ == '__main__':
    make_mappings()
    create_matched_pairs()
