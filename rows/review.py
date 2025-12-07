from sqlmodel import Field, SQLModel


class Row(SQLModel, table=True):
    __tablename__ = "Review"

    product_id: int = Field(primary_key=True)
    owner_id: int = Field(primary_key=True)
    rating: int = Field(ge=1, le=5)
    comment: str
