from subprocess import check_output

from fastapi import FastAPI
from pydantic import BaseModel


def get_poetry_version() -> str:
    """Assume poetry is installed and version is defined"""
    try:
        return check_output(['poetry', 'version', '--short'], encoding='utf-8').rstrip()
    except FileNotFoundError:
        return "unknown version"


app = FastAPI(description="Example app", version=get_poetry_version())


class Item(BaseModel):
    name: str
    price: float
    short_desc: str = ""
    description: str | None = None
    tax: float | None = None
    tags: list[str] = []
    

@app.post("/items/", tags=["Items"])
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/", tags=["Items"])
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
