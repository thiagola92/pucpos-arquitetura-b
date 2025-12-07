from pwdlib import PasswordHash
from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from engine import engine
from bodies.token import PostBody
from rows.user import Row
from auth import create_access_token


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter()
hasher = PasswordHash.recommended()


@router.post("/token")
def post(body: PostBody):
    with Session(engine) as session:
        statement = select(Row).where(Row.username == body.username)
        user = session.exec(statement).first()

    if user is None:
        raise CREDENTIALS_EXCEPTION

    if not hasher.verify(body.password, user.password_hash):
        raise CREDENTIALS_EXCEPTION

    access_token = create_access_token(user.username)

    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
    return {"access_token": access_token, "token_type": "bearer"}
