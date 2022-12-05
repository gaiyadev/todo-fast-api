from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from app import models, schema
from app.database import get_db
from app.dependencies import get_current_user


def create(request: schema.Todo, response, db: Session = Depends(get_db),
           current_user: schema.User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.title == request.title).first()
    if todo:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "todo already exist",
            'status_code': 409,
            'error': 'CONFLICT'
        }

    new_todo = models.Todo(title=request.title, user_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {
        'message': "success",
        'status_code': 201,
        'status': 'Success',
        'data': {
            'id': new_todo.id,
            'email': new_todo.title
        }
    }


def get_all(db: Session):
    todos = db.query(models.Todo).all()
    return todos


def show(post_id: int, response, db: Session = Depends(get_db)):
    todo: models.Todo = db.query(models.Todo).filter(models.Todo.id == post_id).first()
    if not todo:
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
        'data': todo
    }
