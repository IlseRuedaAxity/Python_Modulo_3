from abc import ABC, abstractmethod

from orders.domain.repositories import OrderRepository


class UnitOfWork(ABC):
    """
    Gestiona la transacción completa.
    Garantiza que todo se guarda junto o nada se guarda.
    """
    orders: OrderRepository

    @abstractmethod
    def __enter__(self) -> "UnitOfWork": ...

    @abstractmethod
    def __exit__(self, *args) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...