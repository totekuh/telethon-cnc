from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

prompt_prefix = ''
current_user = ''
current_dir = ''


class PuppetMessage(BaseModel):
    user: str
    pwd: str
    system_encoding: str
    data: str


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.post("/items/{item_id}")
# def create_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# ===================================================================
@app.post('/communicate')
def log(puppet_message: PuppetMessage):
    user = puppet_message.user
    pwd = puppet_message.pwd
    puppet_encoding = puppet_message.system_encoding
    data = puppet_message.data

    #  fixme: finish this crap