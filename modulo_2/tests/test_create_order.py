import pytest
from orders.application.use_cases import CreateOrder, ListOrders, DeleteOrder
from orders.infrastructure.repository_memory import InMemoryUnitOfWork


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


def test_list_orders_returns_all(uow):
    use_case_create = CreateOrder(uow=uow, event_handler=lambda e: None)
    use_case_list = ListOrders(uow=uow)

    use_case_create.execute(
        customer_name="Carlos López",
        items_data=[{"product_name": "Teclado", "quantity": 1, "unit_price": 80.0}],
    )
    use_case_create.execute(
        customer_name="María Torres",
        items_data=[{"product_name": "Monitor", "quantity": 1, "unit_price": 300.0}],
    )

    orders = use_case_list.execute()
    assert len(orders) == 2


def test_delete_order(uow):
    use_case_create = CreateOrder(uow=uow, event_handler=lambda e: None)
    use_case_delete = DeleteOrder(uow=uow)

    result = use_case_create.execute(
        customer_name="Luis Pérez",
        items_data=[{"product_name": "Silla", "quantity": 1, "unit_price": 150.0}],
    )

    deleted = use_case_delete.execute(order_id=result["id"])
    assert deleted is True


def test_delete_order_not_found(uow):
    use_case_delete = DeleteOrder(uow=uow)
    deleted = use_case_delete.execute(order_id="00000000-0000-0000-0000-000000000000")
    assert deleted is False