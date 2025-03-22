"""Various utils for working with files."""

import hashlib
import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar

import magic

from .core.utils import PathLikeType

_C = TypeVar('_C', bound=Callable)


def save_to_json(data: Any, file_path: PathLikeType) -> None:
    """
    Save data to a JSON file.

    :param data: The data to save.
    :param file_path: Path to the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_from_json(file_path: PathLikeType) -> Any:
    """
    Load data from a JSON file.

    :param file_path: Path to the JSON file.
    :return: The loaded data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def cache(cache_file: PathLikeType) -> Callable[[_C], _C]:
    """
    Decorate a function to cache its output to a JSON file.

    :param cache_file: Path to the cache file.
    :return: Decorated function with caching.
    """

    def decorator(func: _C) -> _C:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Path(cache_file).is_file():
                print(f'Using cached {cache_file}')
                return load_from_json(cache_file)
            else:
                res = func(*args, **kwargs)
                save_to_json(res, cache_file)
                return res

        return wrapper  # type: ignore[return-value]

    return decorator


def hash_files(*paths: PathLikeType, hash_length: int = 8) -> str:
    """
    Compute an MD5 hash for the given files.

    :param paths: Paths to the files to be hashed.
    :param hash_length: Length of the returned hash string (default: 8).
    :return: The computed hash string.
    """
    digest_obj = hashlib.md5()
    buffer_size = 2**18

    buffer = bytearray(buffer_size)  # Reusable buffer to reduce allocations.
    view = memoryview(buffer)

    for path in paths:
        with open(path, 'rb') as f:
            while size := f.readinto(buffer):
                digest_obj.update(view[:size])

    return digest_obj.hexdigest()[:hash_length]


def is_text_plain(file_path: PathLikeType) -> bool:
    """
    Check if a file is a plain text file based on its MIME type.

    :param file_path: Path to the file.
    :return: True if the file is plain text, False otherwise.
    """
    return magic.from_file(file_path, mime=True) == 'text/plain'


def is_audio(file_path: PathLikeType) -> bool:
    """
    Check if a file is an audio file based on its MIME type.

    :param file_path: Path to the file.
    :return: True if the file is an audio file, False otherwise.
    """
    return magic.from_file(file_path, mime=True).split('/')[0] == 'audio'


def get_audio_files(dir_path: PathLikeType) -> list[Path]:
    """
    Retrieve a sorted list of audio files from a directory.

    :param dir_path: Path to the directory.
    :return: A sorted list of audio file paths.
    """
    return sorted([p for p in Path(dir_path).iterdir() if p.is_file() and is_audio(p)])
