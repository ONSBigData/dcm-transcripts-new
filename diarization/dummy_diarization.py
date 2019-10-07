
# ---------------------------------------------------------------------
# --- Public
# ---------------------------------------------------------------------


def diarize(segments):
    for s in segments:
        s['speaker_id'] = 0

        if 'type' in s:
            s['speaker_id'] = 0 if s['type'] == 'Male' else 1

    return segments

