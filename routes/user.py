from pwdlib import PasswordHash
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from engine import engine
from rows.user import Row
from bodies.user import PostBody, PostResponse


router = APIRouter()
hasher = PasswordHash.recommended()


@router.post("/user")
def post(body: PostBody):
    user = Row(
        username=body.username,
        email=body.email,
        password_hash=hasher.hash(body.password),
    )

    try:
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)

        return PostResponse(**user.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already in use")
