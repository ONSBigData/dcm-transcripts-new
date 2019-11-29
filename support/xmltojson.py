"""
Script to convert XML transcripts from ICSI to JSON equivalents. Also produces abbreviations.txt which lists all
abbreviations present which might not changing.
"""

import json
from common import *
import xml.etree.ElementTree as ET
import re
import string

FPATH = from_data_root('recordings/icsi/')[:-1]
ORIGINAL_TRANSCRIPT_FPATH = f'{FPATH}/transcripts/'
LETTER_STRING_SEARCH = r"\w+|[^\w\s]"
ABBREVIATION_SEARCH = r"\w+_\w+"
ABBREVIATIONS = []


def get_mrt_files(path):
    file_names = [fn for fn in os.listdir(path) if fn.endswith(".mrt")]

    return file_names


def process_mrt_files(mrt_path):
    json_transcript = {
        "name": None,
        "segments": [

        ]
    }

    mrt_file = ET.parse(mrt_path)
    root = mrt_file.getroot()
    json_transcript["name"] = root.attrib["Session"]

    # Creating a new encoding for speakers
    speaker_lookup = {speaker.attrib["Name"]: i for i, speaker in
                      enumerate(root.iter("Participant"))}

    # Gets each segment (clip of sound) and creates corresponding JSON entry
    for child1 in root.iter('Segment'):
        segment = {
            "start_s": float(child1.attrib["StartTime"]),
            "end_s": float(child1.attrib["EndTime"]),
            "type": "NotAvailable"
        }

        # If there are annotations in transcript they don't contain a participant tag
        if "Participant" in child1.attrib.keys():
            segment["speaker_id"] = speaker_lookup[child1.attrib["Participant"]]

        # Calling .text on just an XML tag with no interior text will return None
        if not str(child1.text) == "None":
            child1_text = str(child1.text)
        else:
            child1_text = ""

        # If there are tags within the text element that also contain text they will be ignored if not pulled out
        for child in child1:
            if not str(child.text) == "None":
                child1_text += child.text

        text = " ".join(child1_text.split())
        segment["words"] = []

        # In some cases there are empty text segments which we don't want
        if len(text) > 1:
            for item in re.findall(LETTER_STRING_SEARCH, text):
                word = {
                    "word": item,
                    "confidence": "NotAvailable",
                    "others": {}
                }

                if item in string.punctuation:
                    word["others"]["type"] = "punctuation"
                else:
                    word["others"]["type"] = "pronunciation"

                segment["words"].append(word)
            if len(re.findall(ABBREVIATION_SEARCH, text)) > 0:
                ABBREVIATIONS.append(re.findall(ABBREVIATION_SEARCH, text))
        else:
            segment["type"] = "noEnergy"

        json_transcript["segments"].append(segment)

    return json_transcript


if __name__ == "__main__":
    mrt_files = get_mrt_files(ORIGINAL_TRANSCRIPT_FPATH)

    for transcript in mrt_files:
        print(transcript)
        json_file = process_mrt_files(f"{ORIGINAL_TRANSCRIPT_FPATH}/{transcript}")

        with open(f'{ORIGINAL_TRANSCRIPT_FPATH}/{transcript[:-4]}.json', 'w') as fp:
            json.dump(json_file, fp)

    flattened_abbreviations = [item for sublist in ABBREVIATIONS for item in sublist]
    set_abbreviations = set(flattened_abbreviations)

    with open(f'{ORIGINAL_TRANSCRIPT_FPATH}/abbreviations.txt', 'w') as f:
        for abb in set_abbreviations:
            f.write(abb + "\n")
