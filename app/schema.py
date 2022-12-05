from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    email: str
    password: str


class Todo(BaseModel):
    title: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int
