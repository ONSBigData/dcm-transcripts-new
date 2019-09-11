import ffmpeg


def convert_audio(from_file, to_file):
    stream = ffmpeg.input(from_file)
    stream = ffmpeg.output(stream, to_file)
    ffmpeg.run(stream)
