from typing import Annotated, Dict, List

from fastapi import APIRouter, Depends, Response, status
from fastapi.params import Query
from fastapi_users_db_sqlalchemy import UUID_ID
from icecream import ic
from jose import jwt
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.dependencies import AuthHandler
from src.config import SECRET_KEY, ALGORITHM
from src.database import get_async_session
from src.my_awesome_sockets import sio_server
from src.orders.models import Order
from src.orders.schemas import Order as OrderScheme, OrderToken, OrderId

order_router = APIRouter(
    prefix='/order',
    tags=['Order'],
)

auth_handler = AuthHandler()

@order_router.get("/get_orders")
async def get_all_orders(
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
        # user: Annotated[UUID_ID | None, Query(max_length=50)] = None
) -> List[OrderScheme]:
    # if user is None:
    #     stmt = select(Order).order_by(
    #         Order.time_created
    #     )
    # else:
    #     stmt = select(Order).where(
    #         Order.user_id == user
    #     ).order_by(
    #         Order.time_created
    #     )

    stmt = select(Order).where(Order.is_active == True).order_by(Order.time_created)

    orders = await db_session.execute(stmt)
    return list(orders.scalars().all())


@order_router.get("/get_orders_for_curr_user")
async def orders_curr_user(
        curruser: Annotated[User, Depends(auth_handler.get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
):
    stmt = (select(Order)
            .where(
                Order.username == curruser.username, Order.is_active == True)
            .order_by(
                Order.priority, Order.time_created
    ))

    orders = await db_session.execute(stmt)
    orders = orders.unique()
    return list(orders.scalars().all())


@order_router.post("/new_order")
async def create_order(
        token: OrderToken,
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Response:
    payload: dict = jwt.decode(token.token, SECRET_KEY, algorithms=[ALGORITHM])

    stmt = insert(Order).values(
        video_id=payload["video_id"],
        title=payload['title'],
        length=payload['length'],
        sendler=payload["sendler"],
        username=payload["username"],
        is_active=payload["is_active"],
        priority=payload["priority"]
    ).returning(Order)

    result = (await db_session.execute(stmt)).scalar_one_or_none()

    order = OrderScheme.model_validate(result)

    await sio_server.emit(data=order.model_dump(mode='json'), event='new_post')

    await db_session.commit()

    return Response("Order has been successfully created", status.HTTP_201_CREATED)


@order_router.post("/delete")
async def delete_order(
        order_id: OrderId,
        curruser: Annotated[User, Depends(auth_handler.get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Response:
    stmt = update(Order).where(Order.id == order_id.order_id, Order.user == curruser).values(is_active=False)
    await db_session.execute(stmt)
    await db_session.commit()
    return Response("Order has been successfully deleted", status.HTTP_200_OK)


@order_router.post("/clear_list")
async def delete_order_list(
        curruser: Annotated[User, Depends(auth_handler.get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Response:
    stmt = update(Order).where(Order.user_id == curruser.id).values(is_active=False)
    await db_session.execute(stmt)
    await db_session.commit()
    return Response("Orders has been successfully deleted", status.HTTP_200_OK)
