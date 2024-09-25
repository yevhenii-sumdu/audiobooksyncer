import functools
import multiprocessing as mp

import ffmpeg


@functools.cache
def get_audio_duration(audio_path):
    return float(ffmpeg.probe(audio_path)['format']['duration'])


def run_in_subprocess(func):
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
