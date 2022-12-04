from fastapi import FastAPI
import models
from database import engine
from routers import user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
