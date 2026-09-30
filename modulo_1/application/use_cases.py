from datetime import datetime, timezone
from domain.entities import Order, OrderItem
from domain.events import OrderCreated
from application.unit_of_work import UnitOfWork
from application.presenter import OrderPresenter
from typing import Callable


class CreateOrder:
    """
    Caso de uso: Crear una nueva orden.
    - Crea la entidad
    - La persiste via UoW
    - Publica el evento OrderCreated
    - Retorna la vista formateada via Presenter
    """

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
            occurred_at=datetime.now(timezone.utc),
        )
        self.event_handler(event)

        # 4. Retornar vista formateada
        return OrderPresenter.to_dict(order)