from collections.abc import Callable
from datetime import UTC, datetime

from orders.application.presenter import OrderPresenter
from orders.application.unit_of_work import UnitOfWork
from orders.domain.entities import Order, OrderItem
from orders.domain.events import OrderCreated


class CreateOrder:
    """Caso de uso: Crear una nueva orden."""

    def __init__(
        self,
        uow: UnitOfWork,
        event_handler: Callable[[OrderCreated], None],
    ):
        self.uow = uow
        self.event_handler = event_handler

    def execute(self, customer_name: str, items_data: list[dict]) -> dict:
        # 1. Construir entidad
        order = Order(customer_name=customer_name)
        for item in items_data:
            order.add_item(OrderItem(**item))

        # 2. Persistir con UoW
        with self.uow:
            self.uow.orders.save(order)
            self.uow.commit()

        # 3. Publicar evento de dominio
        event = OrderCreated(
            order_id=order.id,
            customer_name=order.customer_name,
            total=order.total,
            occurred_at=datetime.now(UTC),
        )
        self.event_handler(event)

        # 4. Retornar vista formateada
        return OrderPresenter.to_dict(order)


class ListOrders:
    """Caso de uso: Listar todas las órdenes."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self) -> list[dict]:
        with self.uow:
            orders = self.uow.orders.list_all()
            self.uow.commit()
        return [OrderPresenter.to_dict(o) for o in orders]


class DeleteOrder:
    """Caso de uso: Eliminar una orden por ID."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, order_id: str) -> bool:
        from uuid import UUID
        with self.uow:
            order = self.uow.orders.get_by_id(UUID(order_id))
            if not order:
                return False
            self.uow.orders.delete(UUID(order_id))
            self.uow.commit()
        return True