import getopt
import json
import shutil
import sys
from pathlib import Path

from file_mapper import generate_file_mapping

OUTPUT_PATH = Path("build")
NOTEBOOKS_PATH = OUTPUT_PATH.joinpath("notebooks")
TEMPLATES_PATH = Path("templates")

def main():
    source_path = resolve_source_path()

    print(f"Creating build path: {OUTPUT_PATH} . . .")
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    print("Creating notebooks path . . .")
    NOTEBOOKS_PATH.mkdir(parents=True, exist_ok=True)

    print("Generating file mapping . . .")
    file_mapping = generate_and_save_file_mapping(source_path)

    print("Copying notebooks to build path . . .")
    copy_notebooks(file_mapping, NOTEBOOKS_PATH)

    print("Copying template files to build path . . .")
    copy_template_files(OUTPUT_PATH)

def generate_and_save_file_mapping(source_path: Path) -> dict:
    file_mapping = generate_file_mapping(source_path)
    file_mapping_path = OUTPUT_PATH.joinpath("file_mapping.json")
    with open(file_mapping_path, "w") as file:
        json.dump(file_mapping, file, indent=4)

    return  file_mapping

def copy_notebooks(file_mapping: dict, destination_path: Path):
    for normalized_name, original_info in file_mapping.items():
        source_path = Path(original_info["original_path"])
        new_file_name = f"{normalized_name}.ipynb"

        copy_file(source_path, destination_path, new_file_name)

def copy_file(source_path: Path, destination_path: Path, new_name: str):
    destination_file = destination_path.joinpath(new_name)

    print(f"Copying {source_path} to {destination_file} . . .")
    shutil.copy2(source_path, destination_file)

def copy_template_files(destination_path: Path):
    # Original names : renames
    template_files = {
        "Dockerfile": "Dockerfile",
        "requirements.txt": "requirements.txt",
        "app_api_template.py": "app.py"
    }

    for source_name, target_name in template_files.items():
        source_path = TEMPLATES_PATH.joinpath(source_name)
        copy_file(source_path, destination_path, target_name)

def resolve_source_path() -> Path:
    source_path = "."
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "s:", ["source_path="])
    except:
        print("Error")

    for opt, arg in opts:
        if opt in ('-s', '--source-path'):
            source_path = arg

    path = Path(source_path)

    # Check if the directory actually exists
    if not path.exists() or not path.is_dir():
        print(f"Error: Directory '{path}' not found.")
        sys.exit(1)

    return path

if __name__ == "__main__":
    main()