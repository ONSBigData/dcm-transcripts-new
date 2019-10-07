from common import *
import ffmpeg
import shutil
import ffmpy
from pydub import AudioSegment


def convert_audio(from_file, to_file):
    ff = ffmpy.FFmpeg(
        inputs={from_file: None},
        outputs={to_file: None}
    )
    ff.run()


def create_audio_slice(from_file, to_file, slice_from_s=None, slice_to_s=None):
    audio = AudioSegment.from_mp3(from_file)

    if slice_from_s is not None or slice_to_s is not None:
        audio = audio[slice_from_s*1000:slice_to_s*1000]

    audio.export(to_file)


def create_audio_slice_in_temp(audio_fpath, slice_from_s=None, slice_to_s=None):
    temp_fpath = from_temp_dir(get_fname_with_ext(audio_fpath))

    create_audio_slice(audio_fpath, temp_fpath, slice_from_s, slice_to_s)

    return temp_fpath


def convert_in_temp_dir(audio_fpath, format='mp3'):
    fname = get_fname_without_ext(audio_fpath)
    temp_fpath = from_temp_dir(f'{fname}.{format}')

    if os.path.exists(temp_fpath):
        os.remove(temp_fpath)

    if audio_fpath.endswith(f'.{format}'):
        shutil.copyfile(audio_fpath, temp_fpath)
    else:
        convert_audio(audio_fpath, temp_fpath)

    return temp_fpath
