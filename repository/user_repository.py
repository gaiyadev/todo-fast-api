from starlette import status
import dependencies
import models

import schema


def sign_up(request, response, db):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "User already exist",
            'status_code': 409,
            'error': 'CONFLICT'
        }

    hash_password = dependencies.hash_password(request.password)
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

    if not (dependencies.verify_password(request.password, user.password)):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }
    #  Generate jwt
    access_token = dependencies.create_access_token(data={"sub": {'email': user.email, 'id': user.id}})
    return {
        'message': 'Success',
        'status_code': 200,
        'data': {
            'email': user.email,
            'id': user.id
        },
        'access_token': access_token
    }
