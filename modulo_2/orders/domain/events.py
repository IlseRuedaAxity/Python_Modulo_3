from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class OrderCreated:
    """Evento de dominio que se dispara cuando una Order es creada."""
    order_id: UUID
    customer_name: str
    total: float
    occurred_at: datetime