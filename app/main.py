from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Message(BaseModel):
    title: str
    content: str
    id: Optional[int] = None
    published: Optional[bool] = True


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi-db',
                                user='badrri',
                                password='secret123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successful")
        break
    except Exception as error:
        print("DB connection unsuccessful")
        print("Error: ", error)
        time.sleep(3)

messages = [
    {"id": 1, "title": "demo1", "content": "this is demo message 1"},
    {"id": 2, "title": "demo2", "content": "this is demo message 2"},
]


@app.get("/messages")
def get_all_messages():
    cursor.execute("""SELECT * FROM tweets;""")
    all_messages = cursor.fetchall()
    return {"data": all_messages}


@app.get("/messages/{message_id}")
def get_message_by_id(message_id: int):
    cursor.execute("""SELECT * FROM tweets where id = %s""", str(message_id))
    retrieved_message = cursor.fetchone()
    if not retrieved_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    return {"data": retrieved_message}


@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: Message):
    cursor.execute("""INSERT INTO tweets (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
                   (message.title, message.content, message.published))
    new_message = cursor.fetchone()
    conn.commit()
    return {"data": new_message}


@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_by_id(message_id: int):
    cursor.execute("""DELETE FROM tweets WHERE id = %s RETURNING *""", str(message_id))
    deleted_message = cursor.fetchone()
    conn.commit()
    if not deleted_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    return {"data": f'message with id {message_id} was deleted'}


@app.put("/messages/{message_id}")
def update_message(message_id: int, message_info: Message):
    cursor.execute("""UPDATE tweets SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (message_info.title, message_info.content, message_info.published, str(message_id)))
    updated_message = cursor.fetchone()
    conn.commit()
    if not updated_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    return {"data": updated_message}
