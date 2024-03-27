import json

from fastapi import FastAPI, HTTPException

import config

app = FastAPI()


@app.get("/{pecha}/texts")
def get_text_list(pecha: str):
    pecha_path = config.DATA_PATH / pecha
    toc_fn = pecha_path / "toc.json"
    if not pecha_path.exists() or not toc_fn.exists():
        return HTTPException(status_code=404, detail="pecha not found")
    toc_fn = pecha_path / "toc.json"
    return json.load(toc_fn.open("r"))


@app.get("/{pecha}/texts/{text_id}/pages")
def get_page_list(pecha: str, text_id: str):
    pecha_path = config.DATA_PATH / pecha
    text_path = pecha_path / text_id
    if not text_path.exists():
        return HTTPException(status_code=404, detail="text not found")
    return list(set([fn.stem for fn in text_path.iterdir()]))
