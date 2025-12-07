from fastapi import FastAPI
from sqlmodel import SQLModel

from engine import engine
from routes.user import router as user
from routes.token import router as login
from routes.review import router as review


app = FastAPI()

app.include_router(user)
app.include_router(login)
app.include_router(review)

SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
