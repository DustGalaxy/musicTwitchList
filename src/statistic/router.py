from typing import Annotated

from fastapi import APIRouter, Depends
from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.dependencies import AuthHandler

from src.database import get_async_session
from src.statistic.schemas import StatGlobalSchemas, StatUserSchemas
from src.statistic import service
# (
#     global_order_count,
#     global_user_count,
#     global_order_popularity,
#     global_sendler_popularity,
#     global_channels_popularity,
#
#     user_order_popularity,
#     user_sendler_popularity,
#     user_count_orders,
#     user_total_time
# )

statistic_router = APIRouter(
    prefix='/stat',
    tags=['Statistic'],
)

auth_handler = AuthHandler()


@statistic_router.get('/global', response_model=StatGlobalSchemas)
async def global_stat(
        days: int,
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StatGlobalSchemas:

    orders_popularity = service.global_order_popularity(days, db_session)

    channels_popularity = service.global_channels_popularity(days, db_session)

    sendler_popularity = service.global_sendler_popularity(days, db_session)

    orders_quantity = service.global_order_count(db_session)
    user_quantity = service.global_user_count(db_session)

    # orders_popularity = await orders_popularity
    # channels_popularity = await channels_popularity
    # sendler_popularity = await sendler_popularity
    # orders_quantity = await orders_quantity
    # user_quantity = await user_quantity

    return StatGlobalSchemas(
        orders_popularity=await orders_popularity,
        channels_popularity=await channels_popularity,
        sendler_popularity=await sendler_popularity,

        user_quantity=await user_quantity,
        orders_quantity=await orders_quantity
    )


@statistic_router.get('/me', response_model=StatUserSchemas)
async def stat_for_curruser(
        days: int,
        curruser: Annotated[User, Depends(auth_handler.get_current_user)],
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StatUserSchemas:
    # stmt = select(User).where(User.username.ilike('nullablelive'))
    #
    # curruser = await db_session.execute(stmt)
    # curruser = curruser.scalar_one()

    orders_popularity = service.user_order_popularity(days=days, user=curruser, db_session=db_session)
    sendler_popularity = service.user_sendler_popularity(days=days, user=curruser, db_session=db_session)

    count_orders = service.user_count_orders(user=curruser, db_session=db_session)
    total_time = service.user_total_time(user=curruser, db_session=db_session)

    # orders_popularity = await orders_popularity
    # sendler_popularity = await sendler_popularity
    # count_orders = count_orders

    total_time = await total_time

    # ic(orders_popularity)
    # ic(sendler_popularity)
    # ic(count_orders)
    # ic(total_time)

    return StatUserSchemas(
        total_time=total_time if total_time is not None else 0,
        orders_quantity=await count_orders,

        sendler_popularity=await sendler_popularity,
        orders_popularity=await orders_popularity,
    )

