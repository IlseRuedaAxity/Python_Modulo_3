from uuid import UUID
from domain.entities import Order
from domain.repositories import OrderRepository
from application.unit_of_work import UnitOfWork


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._store: dict[UUID, Order] = {}

    def save(self, order: Order) -> None:
        self._store[order.id] = order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self._store.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self._store.values())


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.orders = InMemoryOrderRepository()
        self._committed = False

    def __enter__(self) -> "InMemoryUnitOfWork":
        return self

    def __exit__(self, *args) -> None:
        if not self._committed:
            self.rollback()

    def commit(self) -> None:
        self._committed = True

    def rollback(self) -> None:
        self._committed = False