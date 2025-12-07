from pydantic import BaseModel, EmailStr


class PostBody(BaseModel):
    username: str
    email: EmailStr
    password: str


class PostResponse(BaseModel):
    username: str
    email: EmailStr
