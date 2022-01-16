from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    title: str
    content: str
    id: Optional[int] = None
    published: Optional[bool] = True
