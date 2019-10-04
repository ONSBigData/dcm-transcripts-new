from inaSpeechSegmenter import Segmenter


# ---------------------------------------------------------------------
# --- Public
# ---------------------------------------------------------------------


def segment(audio_fpath):
    segmenter = Segmenter()

    segmentation = segmenter(audio_fpath)

    segments = [
        {
            'start_s': s[1],
            'end_s': s[2],
            'type': s[0],
        } for s in segmentation
    ]

    return segments

