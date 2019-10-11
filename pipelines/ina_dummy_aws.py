from pipelines.pipeline import Pipeline
import json
import diarization.dummy_diarization as dummy_dia
import transcription.aws_trancribe as aws_trancribe
from pydub import AudioSegment
from common import *
import multiprocessing as mp

# ---------------------------------------------------------------------
# --- Functions that need to be top-level due to being used in parallelization
# ---------------------------------------------------------------------


def _make_segment(seg, i, audio, target_dir):
    print(f'Making segment {i}')

    seg_audio = audio[seg['start_s'] * 1000: seg['end_s'] * 1000]
    seg_audio_fpath = f"{target_dir}/seg_{i}_audio.mp3"
    seg_audio.export(seg_audio_fpath)

    return seg_audio_fpath


def _get_raw_transcript(seg_audio_fpath, run_id, index):
    print(f'Transcribing {seg_audio_fpath}')

    seg_transcript_raw = aws_trancribe.transcribe(
        seg_audio_fpath,
        'en-GB',
        prefix=f'{run_id}-{index}'
    )

    return seg_transcript_raw

# ---------------------------------------------------------------------
# --- Main class
# ---------------------------------------------------------------------


class InaDummyAwsPipeline(Pipeline):
    def __init__(self, audio_fpath, run_id):
        super().__init__(audio_fpath, run_id)

    def run_segmentation(self, force_rerun=False):
        if not force_rerun and self.load_json('segments'):
            print('Segmentation was alrady run')
            return

        # we only import here cause it's loading some stuff when imported
        import segmentation.ina_segmenter as ina_seg

        all_segments = ina_seg.segment(self.raw_fpath)
        self.save_json(all_segments, 'all_segments')

        segments = [s for s in all_segments if s['type'] != 'NOACTIVITY']
        self.save_json(segments, 'segments')

        return segments

    def run_diarization(self, force_rerun=False):
        if not force_rerun and self.load_json('dia_segments'):
            print('Diarization was alrady run')
            return

        segments = self.load_json('segments')
        if segments is None:
            print('Need to do segmentation first')
            return

        dia_segments = dummy_dia.diarize(segments)
        self.save_json(dia_segments, 'dia_segments')

        return dia_segments

    def run_transcription(self, force_rerun=False):
        if not force_rerun and self.load_json('seg_transcripts'):
            print('Transcription was alrady run')
            return

        segments = self.load_json('segments')
        if segments is None:
            print('Need to do segmentation first')
            return

        # make segments from the audio
        audio = AudioSegment.from_mp3(self.raw_fpath)

        with mp.Pool(20) as pool:
            params = [
                (seg, i, audio, self.pipeline_dir)
                for i, seg in enumerate(segments)
            ]

            seg_audio_fpaths = pool.starmap(_make_segment, params)

        # transcribe them
        with mp.Pool(10) as pool:
            params = [
                (seg_audio_fpath, self.run_id, i)
                for i, seg_audio_fpath in enumerate(seg_audio_fpaths)
            ]
            seg_transcripts_raw = pool.starmap(_get_raw_transcript, params)

        for i, seg_transcript_raw in enumerate(seg_transcripts_raw):
            self.save_json(seg_transcript_raw, f'seg_{i}_transcript_raw')
        self.save_json(seg_transcripts_raw, 'seg_transcripts_raw')

        # extract relevant info from the raw transcripts

        def _extract_words(seg_transcript_raw):
            words = [{
                'word': i['alternatives'][0]['content'],
                'confidence': i['alternatives'][0]['confidence']
            } for i in seg_transcript_raw['results']['items']]

            return words

        seg_transcripts = [
            _extract_words(seg_transcript_raw)
            for seg_transcript_raw in seg_transcripts_raw
        ]
        self.save_json(seg_transcripts, 'seg_transcripts')

        return seg_transcripts

    def create_final(self):
        dia_segments = self.load_json('dia_segments')
        seg_transcripts = self.load_json('seg_transcripts')

        msg = f'lengths mismatch: {len(dia_segments)} != {len(seg_transcripts)}'
        assert len(dia_segments) == len(seg_transcripts), msg

        for i in range(len(dia_segments)):
            dia_segments[i]['words'] = seg_transcripts[i]

        self.save_json(dia_segments, 'final')

        return dia_segments

    def run_all(self, force_rerun=False):
        self.clear_pipeline_dir()

        self.run_segmentation(force_rerun)
        self.run_diarization(force_rerun)
        self.run_transcription(force_rerun)

        self.create_final()


if __name__ == '__main__':
    import recordings.recs as recs
    import support.audiomanip as audiomanip

    r = recs.bbc_interview.load()
    audio_fpath = r.audio_fpath

    slice_to_s = 120
    run_id = f'{path2id(audio_fpath, level_to=-1)}-{slice_to_s}'

    temp_fpath = audiomanip.create_audio_slice_in_temp(
        audio_fpath, 0, slice_to_s
    )

    pipeline = InaDummyAwsPipeline(temp_fpath, run_id)
    pipeline.run_all()


