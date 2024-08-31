import json
import os
from functools import wraps


def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def cache(cache_file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.isfile(cache_file):
                print(f'Using cached {cache_file}')
                return load_from_json(cache_file)
            else:
                res = func(*args, **kwargs)
                save_to_json(res, cache_file)
                return res

        return wrapper

    return decorator
