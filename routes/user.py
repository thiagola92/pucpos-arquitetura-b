from pwdlib import PasswordHash
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

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
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use",
        )

    response = PostResponse(**user.model_dump())

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=response.model_dump(),
    )
