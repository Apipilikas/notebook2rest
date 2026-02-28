#!/usr/bin/env python3
"""
Executed a Jupyter notebook and
    saves the executed notebook as a new file
    or returns it as a JSON string.
"""
from pathlib import Path

from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
import nbformat

class NotebookConverter(Preprocessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.preprocessor = ExecutePreprocessor(timeout=600, kernel_name="python3")

    def execute(self, file_path) -> nbformat.NotebookNode:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook_content = nbformat.read(f, as_version=4)
        executed_np, out_resources = self.preprocessor.preprocess(notebook_content)

        return  executed_np

    def convert_notebook_to_json(self, file_path: Path, user_arg) -> str:
        executed_np = self.execute(file_path)

        return nbformat.writes(executed_np, version=4)

    def convert_notebook_to_ipynb(self, file_path: Path, user_arg) -> Path:
        executed_np = self.execute(file_path)
        executed_file_name = f"{file_path.stem}-executed{file_path.suffix}"
        out_path = file_path.with_name(executed_file_name)

        nbformat.write(executed_np, out_path)

        return out_path