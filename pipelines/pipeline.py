from common import *
import shutil
import json
import os
import glob


class Pipeline:
    def __init__(self, audio_fpath, run_id):
        self.audio_fpath = audio_fpath
        self.run_id = run_id

        print(
            f'Initializing transcribing pipeline "{self.run_id}" '
            f'for {self.audio_fpath}'
        )

        # crete a pipeline dir where we will store all results related
        # to this pipeline run
        self.pipeline_dir = from_data_root(
            f'pipelines/{run_id}/',
            create_if_needed=True
        )[:-1]

        # copy the raw recording to the pipeline dir
        self.raw_fpath = f'{self.pipeline_dir}/raw.mp3'
        shutil.copyfile(audio_fpath, self.raw_fpath)

    def clear_pipeline_dir(self):
        files = glob.glob(f'{self.pipeline_dir}/*')
        print(files)
        for f in files:
            if f == self.raw_fpath:
                continue
            os.remove(f)

    def run_segmentation(self):
        raise NotImplementedError

    def run_diarization(self):
        raise NotImplementedError

    def run_transcription(self):
        raise NotImplementedError

    def run_all(self):
        raise NotImplementedError

    def save_json(self, data, fname):
        fpath = f'{self.pipeline_dir}/{fname}.json'
        with open(fpath, 'w') as f:
            f.write(json.dumps(data))

        return fpath

    def load_json(self, fname):
        fpath = f'{self.pipeline_dir}/{fname}.json'

        if not os.path.exists(fpath):
            return None

        with open(fpath, 'r') as f:
            return json.loads(f.read())



