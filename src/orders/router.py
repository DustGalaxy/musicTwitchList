from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Response, status, Cookie
from fastapi.params import Query
from fastapi_users_db_sqlalchemy import UUID_ID
from jose import jwt
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.models import User
from src.auth.router import get_current_user
from src.config import SECRET_KEY, ALGORITHM
from src.database import get_async_session
from src.orders.models import Order
from src.orders.schemas import Order as OrderScheme, OrderToken

order_router = APIRouter(
    prefix='/order',
    tags=['Order'],
)


@order_router.get("/get_orders/")
async def get_all_orders(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response,
        user: Annotated[UUID_ID | None, Query(max_length=50)] = None,
        cookie: Annotated[str | None, Cookie()] = None

) -> List[OrderScheme]:
    if user is None:
        stmt = select(Order).order_by(
            Order.time_created
        )
    else:
        stmt = select(Order).join(
            User,
            User.username == Order.username
        ).where(
            Order.user_id == user
        ).order_by(
            Order.time_created
        )

    orders = await session.execute(stmt)
    return list(orders.scalars().all())


@order_router.get("/get_orders_for_curr_user")
async def orders_curr_user(
        curruser: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
) -> List[OrderScheme]:
    stmt = select(Order).where(
        Order.username == curruser.username
    ).order_by(
        Order.time_created
    ).options(selectinload(Order.user))

    orders = await session.execute(stmt)
    orders = orders.unique()
    return list(orders.scalars().all())


@order_router.post("/new_order")
async def create_order(
        token: OrderToken,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response
) -> Dict[str, str]:
    payload: dict = jwt.decode(token.token, SECRET_KEY, algorithms=[ALGORITHM])

    stmt = insert(Order).values(
        video_id=payload["video_id"],
        title=payload['title'],
        thumbnailUrl=payload['thumbnail_url'],
        length=payload['length'],
        sendler=payload["sendler"],
        username=payload["username"])

    await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail": "Order has been successfully created"}


@order_router.post("/delete_order")
async def delete_order(
        order_id: UUID_ID,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response
) -> Dict[str, str]:
    stmt = delete(Order).where(Order.id == order_id)
    await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail": "Order has been successfully deleted"}


@order_router.post("/delete_order_many")
async def delete_order(
        id_list: List[UUID_ID],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response
) -> Dict[str, str]:
    for id in id_list:
        stmt = delete(Order).where(Order.id == id)
        await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail": "Orders has been successfully deleted"}


@order_router.post("/clear_order_list")
async def delete_order(
        user_id: UUID_ID,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        response: Response
) -> Dict[str, str]:
    stmt = delete(Order).where(Order.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail": "Orders has been successfully deleted"}
