from common import *
import recordings.prep.harvard.hv_common as hv_common
from support import conversions


def convert_audios():
    if DEF_AUDIO_SUFFIX == '.wav':
        print('no need to convert')
        return

    audio_fpaths = [
        f'{hv_common.DIR_PREP}/{f}'
        for f in os.listdir(hv_common.DIR_PREP) if f.endswith('.wav')
    ]

    for audio_fpath in audio_fpaths:
        dest_audio_fpath = audio_fpath.replace('.wav', DEF_AUDIO_SUFFIX)
        conversions.convert_audio(audio_fpath, dest_audio_fpath)


if __name__ == '__main__':
    convert_audios()
