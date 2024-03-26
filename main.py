import json

from fastapi import FastAPI, HTTPException

import config

app = FastAPI()


@app.get("/{pecha}/texts")
def read_item(pecha: str):
    pecha_path = config.DATA_PATH / pecha
    if not pecha_path.exists():
        return HTTPException(status_code=404, detail="pecha not found")
    toc_fn = pecha_path / "toc.json"
    return json.load(toc_fn.open("r"))
