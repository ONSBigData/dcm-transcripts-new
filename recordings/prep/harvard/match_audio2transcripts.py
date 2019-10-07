from common import *
from support.editdist import levenshtein
import speech_recognition as sr
import recordings.prep.harvard.hv_common as hv_common
import shutil
import re


def find_transcript(audio_fpath, all_transcripts, thresh_ratio=1.7):
    """
    Identifies the matching transcript for the audio file from a pool of
    transcripts. Uses Levenshtein distance to find the most matching transcript.
    The difference in the distance between the best and second best transcripts
    must be large enough. This is controlled by the threshold ratio
    """
    recognizer = sr.Recognizer()

    print(f'\nLooking for the best transcript for {audio_fpath}')
    with sr.AudioFile(audio_fpath) as source:
        audio = recognizer.record(source)

    recog_text = recognizer.recognize_google(audio)

    transcripts = [{
        'transcript_fpath': fpath,
        'text': text,
        'distance': levenshtein(recog_text, text)
    } for fpath, text in all_transcripts.items()]

    transcripts.sort(key=lambda score: score['distance'])

    best_distance = transcripts[0]['distance']
    second_best_distance = transcripts[1]['distance']
    print(f'Best two distances: {best_distance}, {second_best_distance}')

    if best_distance * thresh_ratio > second_best_distance:
        print(f'Did not find a good enough transcript for {audio_fpath}')
        return None

    print(f'Found:\n {transcripts[0]}')
    return transcripts[0]['transcript_fpath']


def get_mappings():
    """
    Returns mapping from audio file path to its transcript (or None, if not
    found)
    """
    text_fpaths = [
        f'{hv_common.DIR_PREP}/{f}'
        for f in os.listdir(hv_common.DIR_PREP)
        if re.search(r'transcript_\d.txt', f)
    ]

    all_transcripts = {}
    for fpath in text_fpaths:
        with open(fpath, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            all_transcripts[fpath] = ' '.join(lines)

    audio_fpaths = [
        f'{hv_common.DIR_PREP}/{f}'
        for f in os.listdir(hv_common.DIR_PREP) if f.endswith('.mp3')
    ]

    mapping = {
        audio_fpath: find_transcript(audio_fpath, all_transcripts)
        for audio_fpath in audio_fpaths
    }

    return mapping


def create_matched_pairs():
    mapping = get_mappings()

    for audio_fpath, transcript_fpath in mapping.items():
        if transcript_fpath is None:
            continue
        fname = os.path.basename(audio_fpath).replace('.mp3', '')
        shutil.copyfile(audio_fpath, f'{hv_common.DIR}/{fname}.mp3')
        shutil.copyfile(transcript_fpath, f'{hv_common.DIR}/{fname}.txt')


if __name__ == '__main__':
    create_matched_pairs()
