from fastapi import FastAPI
from sqlmodel import SQLModel

from engine import engine
from routes.review import router as review


app = FastAPI()

app.include_router(review)

SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
