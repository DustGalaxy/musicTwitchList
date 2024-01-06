from http.client import HTTPResponse
from typing import Annotated, Dict, List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.orders.models import Order
from src.orders.schemas import Order as OrderScheme

from fastapi_users_db_sqlalchemy.generics import GUID

from src.database import get_async_session
from src.auth.models import User
from src.auth.router import get_current_user


order_router = APIRouter(
    prefix='/order',
    tags=['Order'],
)


@order_router.get("/get_orders_for_curr_user")
async def orders_curr_user(
    curruser: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> List[OrderScheme]:
    stmt = select(Order).where(Order.user_id == curruser.id).order_by(Order.time_created)
    orders = await session.execute(stmt)
    orders = orders.unique()
    return orders.scalars().all()
    
    
@order_router.post("/new_order")
async def create_order(
    url: str,
    sendler: str,
    # !!! не curruser а пользователь переданий внутрь запросом от бота
    curruser: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    response: Response
) -> Dict[str, str]:
    stmt = insert(Order).values(url=url, sendler=sendler, user_id=curruser.id)  
    await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"detail": "Order has been successfully created"}