from typing import Optional
from uuid import uuid4
from enum import Enum
from fastapi import FastAPI, Request, Header
from pydantic import BaseModel

app = FastAPI()

prompt_prefix = ''
current_user = ''
current_dir = ''

tasks_queue = []


class TaskType(Enum):
    SHELL_EXEC = 1


class PuppetTask:
    def __init__(self, session_id: str, task_type: TaskType, command: str):
        self.session_id = session_id
        self.task_type = task_type
        self.command = command


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
@app.get('/input')
def log(request: Request, session_id: Optional[str] = Header(None)):
    for task in tasks_queue:
        if task.session_id == session_id:
            return {'task': task.task_type,
                    'command': task.command}


@app.post('/output')
def log(puppet_message: PuppetMessage):
    user = puppet_message.user
    pwd = puppet_message.pwd
    puppet_encoding = puppet_message.system_encoding
    data = puppet_message.data

    #  fixme: finish this crap
