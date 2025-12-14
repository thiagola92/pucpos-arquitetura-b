from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

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

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No review, from this user, found for this product",
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=review.model_dump(),
    )


@router.post("/review/")
def post(body: PostBody, token: Annotated[AccessToken, Depends(get_access_token)]):
    review = Row(
        product_id=body.product_id,
        owner_id=token.user_id,
        rating=body.rating,
        comment=body.comment,
    )

    try:
        with Session(engine) as session:
            session.add(review)
            session.commit()
            session.refresh(review)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exist",
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=review.model_dump(),
    )


@router.put("/review/{product_id}")
def put(body: PutBody, token: Annotated[AccessToken, Depends(get_access_token)]):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == body.product_id,
            Row.owner_id == token.user_id,
        )

        review = session.exec(statement).first()

        if review is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=review.model_dump(),
            )

        review.rating = body.rating
        review.comment = body.comment

        session.commit()
        session.refresh(review)

        return JSONResponse(status_code=status.HTTP_200_OK, content="")


@router.delete("/review/{product_id}")
def delete(product_id: int, token: Annotated[AccessToken, Depends(get_access_token)]):
    with Session(engine) as session:
        statement = select(Row).where(
            Row.product_id == product_id,
            Row.owner_id == token.user_id,
        )

        review = session.exec(statement).first()

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No review, from this user, found for this product",
            )

        session.delete(review)
        session.commit()

        return JSONResponse(status_code=status.HTTP_200_OK, content="")
