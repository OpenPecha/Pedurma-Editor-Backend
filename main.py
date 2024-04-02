import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

import config
from s3 import get_pedurma_image_url

app = FastAPI()

origins = ["http://localhost:9000", "https://pedurma-editor.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Text(BaseModel):
    id: str
    title: str


class PageRead(BaseModel):
    id: str
    image_url: HttpUrl
    content: str


class PageWrite(BaseModel):
    content: str


@app.get("/{pecha}/texts")
def get_text_list(pecha: str) -> list[Text]:
    pecha_path = config.DATA_PATH / pecha
    toc_fn = pecha_path / "toc.json"
    if not pecha_path.exists() or not toc_fn.exists():
        return HTTPException(status_code=404, detail="pecha not found")
    toc_fn = pecha_path / "toc.json"
    toc_dict = json.load(toc_fn.open("r"))
    text_list = []
    for text_id, text_title in toc_dict.items():
        text_list.append(Text(id=text_id, title=text_title))
    return text_list


@app.get("/{pecha}/{text_id}/pages")
def get_page_list(pecha: str, text_id: str) -> list[str]:
    pecha_path = config.DATA_PATH / pecha
    text_path = pecha_path / text_id
    if not text_path.exists():
        return HTTPException(status_code=404, detail="text not found")
    return list(set([fn.stem for fn in text_path.iterdir()]))


@app.get("/{pecha}/{text_id}/{page_id}")
def read_page(pecha: str, text_id: str, page_id: str) -> PageRead:
    pecha_path = config.DATA_PATH / pecha
    text_path = pecha_path / text_id
    page_content_fn = text_path / f"{page_id}.txt"
    page_img_fn = text_path / f"{page_id}.img"
    page_image_name = page_img_fn.read_text().strip()
    page_image_url = get_pedurma_image_url(page_image_name)
    page_content = page_content_fn.read_text().strip()

    return PageRead(id=page_id, image_url=page_image_url, content=page_content)


@app.post("/{pecha}/{text_id}/{page_id}")
def write_page(pecha: str, text_id: str, page_id: str, page: PageWrite):
    pecha_path = config.DATA_PATH / pecha
    text_path = pecha_path / text_id
    page_content_fn = text_path / f"{page_id}.txt"
    page_content_fn.write_text(page.content)
    return {"message": "success"}
