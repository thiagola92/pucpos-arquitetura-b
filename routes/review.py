from fastapi import APIRouter
from sqlmodel import Session, select

from engine import engine
from rows.review import Row
from bodies.review import PostBody, PutBody


router = APIRouter()


@router.get("/review/{product_id}")
def get(product_id: int):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == product_id,
            Row.owner_id == 0,
        )

        review = session.exec(statement).first()

    return review


@router.post("/review/")
def post(body: PostBody):
    review = Row(
        product_id=body.product_id,
        owner_id=0,
        rating=body.rating,
        comment=body.comment,
    )

    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)

    return review


@router.put("/review/{product_id}")
def put(body: PutBody):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == body.product_id,
            Row.owner_id == 0,
        )

        review = session.exec(statement).first()

        if review:
            review.rating = body.rating
            review.comment = body.comment

            session.commit()
            session.refresh(review)

            return review
    return 404


@router.delete("/review/{product_id}")
def delete(product_id: int):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == product_id,
            Row.owner_id == 0,
        )

        review = session.exec(statement).first()

        if review:
            session.delete(review)
            session.commit()
            return 204
        return 404
