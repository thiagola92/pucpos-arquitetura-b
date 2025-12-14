import os
from typing import Annotated
from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer

from engine import engine
from rows.user import Row


# Remember to get your own secret key running "openssl rand -hex 32"
# and to set the environment variable with your key.
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "c9748fb9ce9eaa2dcb763ca01ee8062d20c47783260ab9216e1371e21ff99e91"
)

ALGORITHM = "HS256"
DEFAULT_DURATION = timedelta(hours=1)
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AccessToken(BaseModel):
    user_id: int | None = Field(default=None)
    username: str
    expire: str
    data: dict


def create_access_token(
    username: str,
    duration: timedelta | None = None,
    data: dict = {},
) -> str:
    if duration:
        expire = datetime.now(timezone.utc) + duration
    else:
        expire = datetime.now(timezone.utc) + DEFAULT_DURATION

    payload = AccessToken(
        username=username,
        expire=str(expire),
        data=data.copy(),
    ).model_dump()

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    print("create_access_token", "payload", payload)
    print("create_access_token", "token", token)

    return token


async def open_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AccessToken:
    try:
        print("open_access_token", "token", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("open_access_token", "payload", payload)
        print(payload)
        return AccessToken(**payload)
    except InvalidTokenError as e:
        print("open_access_token", "token", "error", token)
        print(e)
        raise CREDENTIALS_EXCEPTION


def get_access_token(
    access_token: Annotated[AccessToken, Depends(open_access_token)],
) -> AccessToken:
    with Session(engine) as session:
        statement = select(Row).where(Row.username == access_token.username)
        user = session.exec(statement).first()

    if user is None:
        raise CREDENTIALS_EXCEPTION

    access_token.user_id = user.id
    return access_token
