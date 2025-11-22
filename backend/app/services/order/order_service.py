from datetime import datetime, timedelta
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.book_copy import BookCopy
from models.order import Order


async def create_order_service(user_id: int, copy_ids: List[int], db: AsyncSession) -> Order:
    result = await db.execute(select(BookCopy).where(BookCopy.id.in_(copy_ids)))
    copies = result.scalars().all()

    if len(copies) != len(copy_ids):
        raise HTTPException(status_code=404, detail="Некоторые экземпляры книг не найдены")

    for copy in copies:
        if copy.status != "available":
            raise HTTPException(status_code=400, detail=f"Экземпляр {copy.inventory_number} недоступен")
        copy.status = "reserved"
        db.add(copy)

    order = Order(
        user_id=user_id,
        created_at=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        is_active=True,
        is_issued=False,
        copies=copies,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def list_user_orders_service(user_id: int, db: AsyncSession) -> Sequence[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.copies))
        .where(Order.user_id == user_id, Order.is_active == True)
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()


async def list_all_orders_service(db: AsyncSession) -> Sequence[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.copies))
        .where(Order.is_active == True)
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()


async def get_order_service(order_id: int, db: AsyncSession) -> Order:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.copies))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


async def issue_order_service(order_id: int, db: AsyncSession) -> Order:
    order = await get_order_service(order_id, db)
    if order.is_issued:
        raise HTTPException(status_code=400, detail="Заказ уже выдан")

    for copy in order.copies:
        copy.status = "issued"
        db.add(copy)

    order.is_issued = True
    order.issued_at = datetime.now()
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def return_order_service(order_id: int, db: AsyncSession) -> Order:
    order = await get_order_service(order_id, db)
    if not order.is_issued:
        raise HTTPException(status_code=400, detail="Заказ ещё не выдан")
    if not order.is_active:
        raise HTTPException(status_code=400, detail="Заказ уже закрыт")

    for copy in order.copies:
        copy.status = "available"
        db.add(copy)

    order.is_active = False
    order.returned_at = datetime.now()
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def prolong_order_service(order_id: int, user_id: int, db: AsyncSession) -> Order:
    order = await get_order_service(order_id, db)

    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Нельзя продлить чужой заказ")
    if not order.is_active:
        raise HTTPException(status_code=400, detail="Нельзя продлить закрытый заказ")

    order.due_date = order.due_date + timedelta(days=7)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order
