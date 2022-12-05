from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import users_router
from app.routers import todos_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router.router)
app.include_router(todos_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
