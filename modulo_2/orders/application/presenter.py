from orders.domain.entities import Order


class OrderPresenter:
    """Formatea la entidad Order para devolverla al cliente."""

    @staticmethod
    def to_dict(order: Order) -> dict:
        return {
            "id": str(order.id),
            "customer_name": order.customer_name,
            "status": order.status,
            "total": order.total,
            "items": [
                {
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                    "subtotal": i.subtotal,
                }
                for i in order.items
            ],
            "created_at": order.created_at.isoformat(),
        }