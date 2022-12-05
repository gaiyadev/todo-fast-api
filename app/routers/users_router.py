from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import schema
from app.database import get_db
from app.repository import user_repository

router = APIRouter(prefix="/api/v1/users", tags=["users"], )


@router.post('/sign_up', status_code=201, tags=['users'])
def sign_up(request: schema.User, response: Response, db: Session = Depends(get_db)):
    return user_repository.sign_up(request, response, db)


@router.post('/sign_in', status_code=200, tags=['users'])
def login(request: schema.User, response: Response, db: Session = Depends(get_db)):
    return user_repository.login(request, response, db)


@router.get("/{user_id}", status_code=200)
def show(user_id: int, response: Response, db: Session = Depends(get_db)):
    return user_repository.show(user_id, response, db)
