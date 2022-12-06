from fastapi import Query
from pydantic import BaseModel, Required, EmailStr, validator
from typing import Union


class User(BaseModel):
    email: Union[str, None] = Query(default=Required)
    password: Union[str, None] = Query(default=Required, min_length=4)


class Todo(BaseModel):
    title: Union[str, None] = Query(default=Required, min_length=2)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int
