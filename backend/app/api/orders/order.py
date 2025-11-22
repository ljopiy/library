from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import CurrentUser, LibrarianUser
from db.session import get_session
from schemas.order import OrderCreate, OrderRead
from services.order.order_service import (
    create_order_service,
    list_user_orders_service,
    prolong_order_service,
    list_all_orders_service,
    get_order_service,
    issue_order_service,
    return_order_service, cancel_order_service, cancel_order_by_librarian_service,
)
from utilits.order_utilits import order_to_schema

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post("/", response_model=OrderRead)
async def create_order(
        data: OrderCreate,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    order = await create_order_service(current_user.id, data.copy_ids, db)
    return order_to_schema(order)


@orders_router.get("/my", response_model=List[OrderRead])
async def list_my_orders(
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    orders = await list_user_orders_service(current_user.id, db)
    return [order_to_schema(o) for o in orders]


@orders_router.put("/{order_id}/prolong", response_model=OrderRead)
async def prolong_order(
        order_id: int,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    order = await prolong_order_service(order_id, current_user.id, db)
    return order_to_schema(order)


@orders_router.get("/", response_model=List[OrderRead])
async def list_orders_for_librarian(
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    orders = await list_all_orders_service(db)
    return [order_to_schema(o) for o in orders]


@orders_router.get("/{order_id}", response_model=OrderRead)
async def get_order(
        order_id: int,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    order = await get_order_service(order_id, db)
    return order_to_schema(order)


@orders_router.put("/{order_id}/issue", response_model=OrderRead)
async def issue_order(
        order_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    order = await issue_order_service(order_id, db)
    return order_to_schema(order)


@orders_router.put("/{order_id}/return", response_model=OrderRead)
async def return_order(
        order_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    order = await return_order_service(order_id, db)
    return order_to_schema(order)


@orders_router.delete("/{order_id}/cancel", response_model=OrderRead)
async def cancel_order(
        order_id: int,
        current_user: CurrentUser,
        db: AsyncSession = Depends(get_session),
):
    order = await cancel_order_service(order_id, current_user.id, db)
    return order_to_schema(order)


@orders_router.delete("/{order_id}/cancel/by", response_model=OrderRead)
async def cancel_order_by_librarian(
        order_id: int,
        current_user: LibrarianUser,
        db: AsyncSession = Depends(get_session),
):
    order = await cancel_order_by_librarian_service(order_id, db)
    return order_to_schema(order)
