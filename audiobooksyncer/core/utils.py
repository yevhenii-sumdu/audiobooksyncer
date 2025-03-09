import functools
import multiprocessing as mp
import os

import ffmpeg

PathLikeType = str | os.PathLike


@functools.cache
def get_audio_duration(audio_path: PathLikeType):
    """
    Get the duration of an audio file.

    :param audio_path: Path to the audio file.
    :return: Duration of the audio file in seconds.
    """
    return float(ffmpeg.probe(audio_path)['format']['duration'])


def run_in_subprocess(func):
    """
    Decorator to execute a function in a separate subprocess.

    :param func: The function to be executed.
    :return: Wrapped function that runs in a subprocess.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def subprocess_function():
            try:
                queue.put(func(*args, **kwargs))
            except Exception as e:
                queue.put(e)

        queue = mp.Queue()

        process = mp.Process(target=subprocess_function, daemon=True)
        process.start()

        result = queue.get()

        process.join()

        if isinstance(result, Exception):
            raise result

        return result

    return wrapper
