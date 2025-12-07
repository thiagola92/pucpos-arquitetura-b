from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from auth import AccessToken, get_access_token
from engine import engine
from rows.review import Row
from bodies.review import PostBody, PutBody


router = APIRouter()


@router.get("/review/{product_id}")
def get(product_id: int, token: Annotated[AccessToken, Depends(get_access_token)]):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == product_id,
            Row.owner_id == token.user_id,
        )

        review = session.exec(statement).first()

    return review


@router.post("/review/")
def post(body: PostBody, token: Annotated[AccessToken, Depends(get_access_token)]):
    review = Row(
        product_id=body.product_id,
        owner_id=token.user_id,
        rating=body.rating,
        comment=body.comment,
    )

    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)

    return review


@router.put("/review/{product_id}")
def put(body: PutBody, token: Annotated[AccessToken, Depends(get_access_token)]):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == body.product_id,
            Row.owner_id == token.user_id,
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
def delete(product_id: int, token: Annotated[AccessToken, Depends(get_access_token)]):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == product_id,
            Row.owner_id == token.user_id,
        )

        review = session.exec(statement).first()

        if review:
            session.delete(review)
            session.commit()
            return 204
        return 404
