from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException

app = FastAPI()


class Message(BaseModel):
    title: str
    content: str
    id: Optional[int] = None


messages = [
    {"id": 1, "title": "demo1", "content": "this is demo message 1"},
    {"id": 2, "title": "demo2", "content": "this is demo message 2"},
]

@app.get("/messages")
def get_all_messages():
    return {"data": messages}


@app.get("/messages/{message_id}")
def get_message_by_id(message_id: int):
    if message_id > len(messages) or message_id < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    return {"data": [p for p in messages if p["id"] == message_id]}


@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: Message):
    new_message = message.dict()
    new_message["id"] = len(messages)+1
    messages.append(new_message)
    return {"data": new_message}


def find_index_of_message(id):
    for i, p in enumerate(messages):
        if p["id"] == id:
            return i
    return -1


@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_by_id(message_id: int):
    index = find_index_of_message(message_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    messages.pop(index)
    return {"data": f'message with id {message_id} was deleted'}


@app.put("/messages/{message_id}")
def update_message(message_id: int, message_info: Message):
    index = find_index_of_message(message_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    messages[index]["title"] = message_info.title
    messages[index]["content"] = message_info.content
    return {"data": "message update successfully"}
