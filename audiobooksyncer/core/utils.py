import os


def get_sorted_files_in_dir(dir_path):
    return sorted([os.path.join(dir_path, f) for f in os.listdir(dir_path)])
