from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class Row(SQLModel, table=True):
    __tablename__ = "User"

    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    email: EmailStr
    password_hash: str
