import json
import os
from support import editdist

ORIGINAL_DIR = os.path.expanduser("~/dcm-transcripts-new/data/recordings/icsi/transcripts")
AUTO_DIR = os.path.expanduser("~/dcm-transcripts-new/data/pipelines/icsi-300")


def evaluate(original_transcript, auto_transcript):
    print("Beginning evaluation")

    print("Evaluating segment amount")
    equal = compare_segments(original_transcript, auto_transcript)

    if equal:
        print("Segment amounts match, comparing text by segment")
        compare_segment_text(original_transcript, auto_transcript)
    else:
        print("Segment amounts do not match, comparing text as one blob")
        distance = compare_full_text(original_transcript, auto_transcript)

        print(f"Levenshtein Distance: {distance}")


def compare_segments(original_transcript, auto_transcript):
    original_length = len(original_transcript["segments"])
    auto_length = len(auto_transcript["segments"])

    print(f"Original Length: {original_length}")
    print(f"Auto Length: {auto_length}")

    if original_length == auto_length:
        equal = True
    else:
        equal = False

    return equal


def compare_segment_text(original_transcript, auto_transcript):
    pass


def compare_full_text(original_transcript, auto_transcript):
    def _create_blob(transcript):
        blob = ""

        for seg in transcript["segments"]:
            for word in seg["words"]:
                if word["others"]["type"] == "pronunciation":
                    blob += f" {word['word']}"
                elif word["others"]["type"] == "punctuation":
                    blob += f"{word['word']}"

            blob += "\n"

        return blob

    original_blob = _create_blob(original_transcript)
    auto_blob = _create_blob(auto_transcript)

    print(f"{len(original_blob)}")
    print(f"{len(auto_blob)}")

    with open(os.path.expanduser("~/original_blob.txt"), 'w') as f:
        f.write(original_blob)

    with open(os.path.expanduser("~/auto_blob.txt"), 'w') as f:
        f.write(auto_blob)

    print("Computing Levenshtein distance")
    distance = editdist.levenshtein(original_blob.strip(), auto_blob.strip())

    return distance


def compare_diarization(original_transcript, auto_transcript):
    pass #TODO: Implement diarization evaluation


def load_transcripts():
    with open(f"{ORIGINAL_DIR}/Bdb001.json", "r") as read_file:
        original_transcript = json.load(read_file)

    with open(f"{AUTO_DIR}/final.json", "r") as read_file:
        auto_transcript = json.load(read_file)

    return original_transcript, auto_transcript


if __name__ == "__main__":
    original_transcript, auto_transcript = load_transcripts()
    evaluate(original_transcript, auto_transcript)

