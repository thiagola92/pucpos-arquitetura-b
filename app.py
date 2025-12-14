from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from engine import engine
from routes.user import router as user
from routes.token import router as login
from routes.review import router as review
from routes.reviews import router as reviews


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(login)
app.include_router(review)
app.include_router(reviews)

SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
