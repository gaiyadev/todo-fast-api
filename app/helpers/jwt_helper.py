import os
from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from jose import JWTError
import jwt as pyjwt
from dotenv import load_dotenv

load_dotenv()
from app import schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = pyjwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
    return encoded_jwt


def verify_token(credentials, credentials_exception):
    try:
        token = credentials.credentials
        payload = pyjwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')])
        user = payload.get('sub')
        if user is None:
            raise credentials_exception
        return schema.TokenData(id=user['id'], email=user['email'])
    except JWTError:
        raise credentials_exception
