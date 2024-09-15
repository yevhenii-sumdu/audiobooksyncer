import functools
import multiprocessing as mp
import os
from typing import Callable, TypeVar

import ffmpeg

C = TypeVar('C', bound=Callable)


def get_sorted_files_in_dir(dir_path):
    return sorted([os.path.join(dir_path, f) for f in os.listdir(dir_path)])


@functools.cache
def get_audio_duration(audio_path):
    return float(ffmpeg.probe(audio_path)['format']['duration'])


def run_in_subprocess(func: C) -> C:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with mp.Pool(1) as pool:
            return pool.apply(func, args, kwargs)

    return wrapper
