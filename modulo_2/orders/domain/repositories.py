from abc import ABC, abstractmethod
from uuid import UUID

from orders.domain.entities import Order


class OrderRepository(ABC):
    """Puerto: interfaz que la infraestructura debe implementar."""

    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    def list_all(self) -> list[Order]: ...

    @abstractmethod
    def delete(self, order_id: UUID) -> None: ...