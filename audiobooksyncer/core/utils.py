import os
import json

def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def get_sorted_files_in_dir(dir_path):
    return sorted([os.path.join(dir_path, f) for f in os.listdir(dir_path)])