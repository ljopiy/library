from models.order import Order
from schemas.order import OrderRead


def order_to_schema(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        user_id=order.user_id,
        created_at=order.created_at,
        due_date=order.due_date,
        issued_at=order.issued_at,
        returned_at=order.returned_at,
        is_active=order.is_active,
        is_issued=order.is_issued,
        copy_ids=[c.id for c in order.copies],
    )
