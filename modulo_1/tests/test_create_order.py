import pytest
from application.use_cases import CreateOrder
from infrastructure.repository_memory import InMemoryUnitOfWork


@pytest.fixture
def uow():
    return InMemoryUnitOfWork()


def test_create_order_returns_correct_total(uow):
    use_case = CreateOrder(uow=uow, event_handler=lambda e: None)

    result = use_case.execute(
        customer_name="Ana García",
        items_data=[
            {"product_name": "Laptop", "quantity": 1, "unit_price": 1500.0},
            {"product_name": "Mouse",  "quantity": 2, "unit_price": 25.0},
        ],
    )

    assert result["customer_name"] == "Ana García"
    assert result["total"] == 1550.0
    assert len(result["items"]) == 2
    assert result["status"] == "pending"


def test_create_order_fires_event(uow):
    events_captured = []

    use_case = CreateOrder(
        uow=uow,
        event_handler=lambda e: events_captured.append(e),
    )

    use_case.execute(
        customer_name="Carlos López",
        items_data=[{"product_name": "Teclado", "quantity": 1, "unit_price": 80.0}],
    )

    assert len(events_captured) == 1
    assert events_captured[0].customer_name == "Carlos López"
    assert events_captured[0].total == 80.0


def test_order_persisted_in_repository(uow):
    use_case = CreateOrder(uow=uow, event_handler=lambda e: None)

    result = use_case.execute(
        customer_name="Luis Pérez",
        items_data=[{"product_name": "Monitor", "quantity": 1, "unit_price": 300.0}],
    )

    from uuid import UUID
    order_id = UUID(result["id"])
    saved_order = uow.orders.get_by_id(order_id)

    assert saved_order is not None
    assert saved_order.customer_name == "Luis Pérez"