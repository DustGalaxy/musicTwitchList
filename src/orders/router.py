from http.client import HTTPResponse
from typing import Annotated, Dict, List
from fastapi import APIRouter, Depends, Response, status
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
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

@order_router.get("/get_orders")
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> List[OrderScheme]:
    stmt = select(Order).join(
                            User, 
                            User.id == Order.user_id
                        ).order_by(Order.time_created
                        ).options(selectinload(Order.user))
                        
    orders = await session.execute(stmt)
    orders = orders.unique()
    return orders.scalars().all()
    

@order_router.get("/get_orders_for_curr_user")
async def orders_curr_user(
    curruser: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> List[OrderScheme]:
    
    stmt = select(Order).join(
                            User, 
                            User.id == Order.user_id
                        ).where(
                            Order.user_id == curruser.id
                        ).order_by(
                            Order.time_created
                        ).options(selectinload(Order.user))
                        
    orders = await session.execute(stmt)
    orders = orders.unique()
    return orders.scalars().all()
    
    
@order_router.post("/new_order")
async def create_order(
    url: str,
    sendler: str,
    # user_id: GUID
    # !!! не curruser а пользователь переданий внутрь запросом от бота
    curruser: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    response: Response
) -> Dict[str, str]:
    stmt = insert(Order).values(url=url, sendler=sendler, user_id=curruser.id)  
    await session.execute(stmt)
    await session.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail": "Order has been successfully created"}


@order_router.post("/delete_order")
async def delete_order(
    id: UUID_ID,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    response: Response
) -> Dict[str, str]:
    stmt = delete(Order).where(Order.id == id)
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