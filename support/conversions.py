from common import *
import ffmpeg
import shutil
import ffmpy


TEMP_DIR = from_data_root('temp/', create_if_needed=True)[:-1]


def convert_audio(from_file, to_file):
    ff = ffmpy.FFmpeg(
        inputs={from_file: None},
        outputs={to_file: None}
    )
    ff.run()


def convert_in_temp_dir(audio_fpath, format='wav'):
    base_name = os.path.basename(audio_fpath)
    fname = '.'.join(base_name.split('.')[:-1])
    temp_fpath = f"{TEMP_DIR}/{fname}.{format}"

    if os.path.exists(temp_fpath):
        os.remove(temp_fpath)

    if audio_fpath.endswith(f'.{format}'):
        shutil.copyfile(audio_fpath, temp_fpath)
    else:
        convert_audio(audio_fpath, temp_fpath)

    return temp_fpath
