from schemas.book import BookRead
from schemas.order import OrderRead


from schemas.book import BookRead

def order_to_schema(order):
    books = [
        BookRead.from_orm(copy.book).copy(
            update={"average_rating": copy.book.calc_average_rating()}
        )
        for copy in order.copies if copy.book
    ]
    return OrderRead.from_orm(order).copy(update={"books": books})
