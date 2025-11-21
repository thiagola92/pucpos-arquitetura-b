from pydantic import BaseModel, Field
from typing import Annotated


class PostBody(BaseModel):
    product_id: Annotated[int, Field(ge=0)]
    rating: Annotated[int, Field(ge=1, le=5)]
    comment: str


class PutBody(BaseModel):
    product_id: Annotated[int, Field(ge=0)]
    rating: Annotated[int, Field(ge=1, le=5)]
    comment: str
