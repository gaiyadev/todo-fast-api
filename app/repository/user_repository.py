from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from app import models, schema
from app.database import get_db
from app.helpers import password_helper
from app.helpers.jwt_helper import create_access_token


def sign_up(request: schema.User, response, db):
    email = db.query(models.User).filter(models.User.email == request.email).first()
    if email:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "User already exist",
            'status_code': 409,
            'error': 'CONFLICT'
        }

    hash_password = password_helper.hash_password(request.password)
    new_user = models.User(email=request.email, password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': new_user.id,
            'email': new_user.email
        }
    }


def login(request: schema.User, response, db):
    user: models.User = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }

    if not (password_helper.verify_password(request.password, user.password)):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }
    #  Generate jwt
    access_token = create_access_token(data={"sub": {'email': user.email, 'id': user.id}})
    return {
        'message': 'Success',
        'status_code': 200,
        'data': {
            'email': user.email,
            'id': user.id
        },
        'access_token': access_token
    }


def show(user_id: int, response, db: Session = Depends(get_db)):
    user: models.User = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT_FOUND'
        }
    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': user
    }
