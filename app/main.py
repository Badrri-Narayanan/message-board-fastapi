from fastapi import FastAPI, status, HTTPException, Depends
import ctypes
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/messages")
def get_all_messages(db: Session = Depends(get_db)):
    all_messages = db.query(models.Message).all()
    return {"data": all_messages}


@app.get("/messages/{message_id}")
def get_message_by_id(message_id: int, db: Session = Depends(get_db)):
    retrieved_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not retrieved_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    return {"data": retrieved_message}


@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(message: schemas.Message, db: Session = Depends(get_db)):
    new_message = models.Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"data": new_message}


@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_by_id(message_id: int, db: Session = Depends(get_db)):
    deleted_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not deleted_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    db.delete(deleted_message)
    db.commit()
    return {"data": f'message with id {message_id} was deleted'}


@app.put("/messages/{message_id}")
def update_message(message_id: int, message_info: schemas.Message, db: Session = Depends(get_db)):
    update_query = db.query(models.Message).filter(models.Message.id == message_id)
    updated_message = update_query.first()
    message_info.id = message_id

    if not updated_message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'message with id {message_id} is not found')
    update_query.update(message_info.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_message)

    return {"data": updated_message}


@app.get("/factorial/{num}")
def find_factorial(num: int):
    c_module = ctypes.CDLL("./app/lib_factorial.so")
    c_module.factorial.argtypes = [ctypes.c_int]
    c_module.factorial.restype = ctypes.c_long
    result = f'Factorial of {num} = {c_module.factorial(num)}'
    return {"result": result}


