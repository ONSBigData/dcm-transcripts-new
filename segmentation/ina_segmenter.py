import warnings

# ---------------------------------------------------------------------
# --- Public
# ---------------------------------------------------------------------


def segment(audio_fpath):
    warnings.filterwarnings("ignore")

    from inaSpeechSegmenter import Segmenter
    segmenter = Segmenter()
    segmentation = segmenter(audio_fpath)

    warnings.resetwarnings()

    segments = [
        {
            'start_s': s[1],
            'end_s': s[2],
            'type': s[0],
        } for s in segmentation
    ]

    return segments

