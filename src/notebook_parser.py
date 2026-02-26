#!/usr/bin/env python3
"""
Executed a Jupyter notebook and
    saves the executed notebook as a new file
    or returns it as a JSON string.
"""

from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
import nbformat

class NotebookConverter(Preprocessor):
    def convert_notebooks_to_python(self, file_path, user_arg):
        with open(file_path, "r", encoding="utf-8") as f:
            notebook_content = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout= 600, kernel_name="python3")
        executed_np, out_resources = ep.preprocess(notebook_content)


        if user_arg == "ipynb":
            out_path = file_path.replace(".ipynb", "_executed.ipynb")
            # Using nbformat.write
            nbformat.write(executed_np, out_path)
        elif user_arg == "json":
            # Using nbformat.writes
            return nbformat.writes(executed_np, version=4)
