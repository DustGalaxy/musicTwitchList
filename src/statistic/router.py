from typing import Annotated

from fastapi import APIRouter, Depends
from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.router import get_current_user

from src.database import get_async_session
from src.statistic.schemas import StatGlobalSchemas, StatUserSchemas
from src.statistic.utils import (
    global_order_count,
    global_user_count,
    global_order_popularity,
    global_sendler_popularity,
    global_channels_popularity,

    user_order_popularity,
    user_sendler_popularity,
    user_count_orders,
    user_total_time
)

statistic_router = APIRouter(
    prefix='/stat',
    tags=['Statistic'],
)


@statistic_router.get('/global')
async def global_stat(
        days: int,
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StatGlobalSchemas:

    orders_popularity = global_order_popularity(days, db_session)

    channels_popularity = global_channels_popularity(days, db_session)

    sendler_popularity = global_sendler_popularity(days, db_session)

    orders_quantity = global_order_count(db_session)
    user_quantity = global_user_count(db_session)

    # orders_popularity = await orders_popularity
    channels_popularity = await channels_popularity
    sendler_popularity = await sendler_popularity
    orders_quantity = await orders_quantity
    user_quantity = await user_quantity

    return StatGlobalSchemas(
        orders_popularity=await orders_popularity,
        channels_popularity=channels_popularity,
        sendler_popularity=sendler_popularity,

        user_quantity=user_quantity,
        orders_quantity=orders_quantity
    )


@statistic_router.get('/me')
async def stat_for_curruser(
        days: int,
        curruser: Annotated[User, Depends(get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StatUserSchemas:
    # stmt = select(User).where(User.username.ilike('nullablelive'))
    #
    # curruser = await db_session.execute(stmt)
    # curruser = curruser.scalar_one()

    orders_popularity = user_order_popularity(days=days, user=curruser, db_session=db_session)
    sendler_popularity = user_sendler_popularity(days=days, user=curruser, db_session=db_session)

    count_orders = user_count_orders(user=curruser, db_session=db_session)
    total_time = user_total_time(user=curruser, db_session=db_session)

    orders_popularity = await orders_popularity
    sendler_popularity = await sendler_popularity
    count_orders = await count_orders
    total_time = await total_time

    # ic(orders_popularity)
    # ic(sendler_popularity)
    # ic(count_orders)
    # ic(total_time)

    return StatUserSchemas(
        total_time=total_time if total_time is not None else 0,
        orders_quantity=count_orders,

        sendler_popularity=sendler_popularity,
        orders_popularity=orders_popularity,
    )

