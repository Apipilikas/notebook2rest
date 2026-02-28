from pathlib import Path
import json
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from notebook_converter import NotebookConverter

NOTEBOOKS_PATH = Path("notebooks")
CONVERTER = NotebookConverter()

app = FastAPI(
    title="Notebook2Rest API",
    description="A notebook2rest API"
)

@app.get("/api/notebooks")
def get_notebooks():
    with open("file_mapping.json", 'r') as file:
        data = json.load(file)
    return {"notebooks": list(data.keys())}

@app.get("/api/notebooks/{notebook_name}/export")
def get_results(notebook_name, request: Request):

    file_path = NOTEBOOKS_PATH.joinpath(f'{notebook_name}.ipynb')

    if file_path is None:
        raise HTTPException(status_code=404, detail="Notebook file cannot be found.")

    accept_header = request.headers.get("Accept", "")

    if "application/x-ipynb+json" in accept_header:
        out_path = CONVERTER.convert_notebook_to_ipynb(file_path, None)

        return FileResponse(
            path=out_path,
            filename=out_path.name,
            media_type="application/x-ipynb+json"
        )
    else:
        result = CONVERTER.convert_notebook_to_json(file_path, None)
        return {"results": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)