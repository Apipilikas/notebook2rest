from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

NOTEBOOKS_PATH = Path("notebooks")

app = FastAPI(
    title="{{ title }} - Notebook2Rest API",
    description="A notebook2rest API"
)

@app.get("/api/notebooks")
def get_notebooks():
    return {"notebooks": []}

class ExportParams(BaseModel):
    type: str
    params: dict[str, object]

@app.post("/api/notebooks/{notebook_name}/export")
def get_results(notebook_name, params: ExportParams):

    file_path = find_file_path(notebook_name)

    if file_path is None:
        raise HTTPException(status_code=404, detail="Notebook file cannot be found.")

    match params.type:
        case "json":
            result = export_notebook_to_json()
            return {"results": result}
        case "ipynb":
            result = export_notebook_to_ipynb()
            return {"results": result}
        case _:
            raise HTTPException(status_code=404, detail="Exported type is not supported.")