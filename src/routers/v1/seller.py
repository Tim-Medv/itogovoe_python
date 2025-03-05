from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations.database import get_async_session
from src.models.sellers import Seller
from src.schemas.seller import (
    IncomingSeller,
    ReturnedSeller,
    ReturnedSellerWithBooks,
    IncomingSellerUpdate,
)
from icecream import ic

seller_router = APIRouter(tags=["seller"], prefix="/seller")

# Регистрация продавца
@seller_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: AsyncSession = Depends(get_async_session)):
    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.email,
        password=seller.password,
    )
    session.add(new_seller)
    await session.flush()  # получение id
    return new_seller

# Получение списка всех продавцов (без поля password)
@seller_router.get("/", response_model=list[ReturnedSeller])
async def get_all_sellers(session: AsyncSession = Depends(get_async_session)):
    query = select(Seller)
    result = await session.execute(query)
    sellers = result.scalars().all()
    return sellers

# Детальный просмотр продавца с его книгами (без пароля)
@seller_router.get("/{seller_id}", response_model=ReturnedSellerWithBooks)
async def get_seller(seller_id: int, session: AsyncSession = Depends(get_async_session)):
    seller = await session.get(Seller, seller_id)
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return seller

# Обновление данных продавца (без изменения книг и пароля)
@seller_router.put("/{seller_id}", response_model=ReturnedSeller)
async def update_seller(seller_id: int, update_data: IncomingSellerUpdate, session: AsyncSession = Depends(get_async_session)):
    seller = await session.get(Seller, seller_id)
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if update_data.first_name is not None:
        seller.first_name = update_data.first_name
    if update_data.last_name is not None:
        seller.last_name = update_data.last_name
    if update_data.email is not None:
        seller.e_mail = update_data.email
    await session.flush()
    return seller

# Удаление продавца вместе с его книгами
@seller_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: AsyncSession = Depends(get_async_session)):
    seller = await session.get(Seller, seller_id)
    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await session.delete(seller)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
