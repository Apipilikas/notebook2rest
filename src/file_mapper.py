import re
from pathlib import Path

def normalize_file_name(file_name: str):
    name = file_name.replace('.ipynb', '')
    name = name.lower()
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'[^a-z0-9\-]', '', name)

    return name.strip('-')

def generate_file_mapping(path: Path):

    mapping = {}

    for specific_path in path.glob("**/*.ipynb"):
        path_name = specific_path.name
        normalized_file_name = normalize_file_name(path_name)

        mapping[normalized_file_name] = {
            "original_name": path_name,
            "original_path": str(specific_path)
        }

    return mapping