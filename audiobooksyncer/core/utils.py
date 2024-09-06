import os

import ffmpeg


def get_sorted_files_in_dir(dir_path):
    return sorted([os.path.join(dir_path, f) for f in os.listdir(dir_path)])


def get_audio_duration(audio_path):
    return float(ffmpeg.probe(audio_path)['format']['duration'])
