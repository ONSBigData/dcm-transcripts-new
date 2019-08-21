

class Recording:
    def __init__(self):
        self.audio_fpath = None
        self.transcript_fpath = None

        self.no_speakers = None

        self.pure_transcript = None  # just text as one blob

        self.structured_transcript = None  # diarized/segmented transcript

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = (
            f'Audio: {self.audio_fpath}\n' +
            f'Transcript: {self.transcript_fpath}\n' +
            f'No speakers: {self.no_speakers}\n\n'
        )

        if self.structured_transcript is not None:
            s += str(self.structured_transcript)
        else:
            s += str(self.pure_transcript)

        s += '\n'

        return s

