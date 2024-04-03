from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.orders.models import Order
from src.statistic.schemas import StatOrderPopularitySchemas, StatChannelPopularitySchemas, StatSendlerPopularitySchemas


async def global_order_popularity(
        days: int,
        db_session: AsyncSession,
):
    stmt = (select(Order.video_id, Order.title, func.count(Order.id)
                   ).join(User).where(
        Order.time_created > datetime.now(timezone.utc) - timedelta(days=days),
        User.in_statistics == True
    ).group_by(Order.video_id, Order.title
               ).order_by(func.count(Order.id).desc()
                          ).limit(20))
    result = await db_session.execute(stmt)

    return [StatOrderPopularitySchemas(
        video_id=i[0],
        title=i[1],
        quantity=i[2]
    ) for i in result.all()]


async def global_order_count(
        db_session: AsyncSession
):
    stmt = select(func.count(Order.id))
    result = await db_session.execute(statement=stmt)
    return result.scalar()


async def global_channels_popularity(
        days: int,
        db_session: AsyncSession
):
    stmt = (select(User.username, func.count(Order.id))
            .join(Order)
            .where(
                Order.time_created > datetime.now(timezone.utc) - timedelta(days=days),
                User.in_statistics == True)
            .group_by(User.username)
            .order_by(func.count(Order.id).desc())
            .limit(20))
    result = await db_session.execute(statement=stmt)

    return [StatChannelPopularitySchemas(
        channel_name=i[0],
        quantity=i[1]
    ) for i in result.all()]


async def global_sendler_popularity(
        days: int,
        db_session: AsyncSession
):
    stmt = select(Order.sendler, func.count(Order.id)
                  ).join(User).where(
        Order.time_created > datetime.now(timezone.utc) - timedelta(days=days),
        User.in_statistics == True
    ).group_by(Order.sendler
               ).order_by(func.count(Order.id).desc()
                          ).limit(20)
    result = await db_session.execute(statement=stmt)

    return [StatSendlerPopularitySchemas(
        sendler_name=i[0],
        quantity=i[1]
    ) for i in result.all()]


async def global_user_count(
        db_session: AsyncSession,
):
    stmt = select(func.count(User.id))
    res = await db_session.execute(stmt)
    return res.scalar()


async def user_order_popularity(
        days: int,
        user: User,
        db_session: AsyncSession,
):
    stmt = (select(Order.video_id, Order.title, func.count(Order.id))
            .join(User)
            .where(Order.time_created > datetime.now(timezone.utc) - timedelta(days=days),
                   User.id == user.id)
            .group_by(Order.video_id, Order.title)
            # .having(func.count(Order.id) >= 0)
            .order_by(func.count(Order.id).desc())
            .limit(20))
    result = await db_session.execute(stmt)

    return [StatOrderPopularitySchemas(
        video_id=i[0],
        title=i[1],
        quantity=i[2]
    ) for i in result.all()]


async def user_sendler_popularity(
        days: int,
        user: User,
        db_session: AsyncSession,
):
    stmt = (select(Order.sendler, func.count(Order.id))
            .join(User)
            .where(Order.time_created > datetime.now(timezone.utc) - timedelta(days=days),
                   User.id == user.id)
            .group_by(Order.sendler)
            # .having(func.count(Order.id) >= 0)
            .order_by(func.count(Order.id).desc())
            .limit(20))
    result = await db_session.execute(statement=stmt)

    return [StatSendlerPopularitySchemas(
        sendler_name=i[0],
        quantity=i[1]
    ) for i in result.all()]


async def user_count_orders(
        user: User,
        db_session: AsyncSession,
):
    stmt = (select(func.count(Order.id))
            .join(User)
            .where(User.id == user.id))
    result = await db_session.execute(statement=stmt)
    return result.scalar()


async def user_total_time(
        user: User,
        db_session: AsyncSession,
):
    stmt = (select(func.sum(Order.length))
            .join(User)
            .where(User.id == user.id))
    result = await db_session.execute(statement=stmt)
    return result.scalar()
