from fastapi import APIRouter, status
from sqlmodel import Session, select
from fastapi.responses import JSONResponse

from engine import engine
from rows.review import Row


router = APIRouter()


@router.get("/reviews/{product_id}")
def get(product_id: int):
    with Session(engine) as session:
        statement = select(Row).where(Row.product_id == product_id)
        reviews = session.exec(statement).fetchall()
        reviews = [r.model_dump() for r in reviews]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=reviews,
    )
