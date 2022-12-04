from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
import schema
from database import get_db
from repository import user_repository

router = APIRouter()


@router.post('/sign_up', status_code=201, tags=['users'])
def sign_up(request: schema.User, response: Response, db: Session = Depends(get_db)):
    return user_repository.sign_up(request, response, db)


@router.post('/login', status_code=200, tags=['users'])
def login(request: schema.User, response: Response, db: Session = Depends(get_db)):
    return user_repository.login(request, response, db)
