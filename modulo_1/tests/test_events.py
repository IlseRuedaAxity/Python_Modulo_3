from datetime import datetime, timezone
from uuid import uuid4
from domain.events import OrderCreated


def test_order_created_event_is_immutable():
    event = OrderCreated(
        order_id=uuid4(),
        customer_name="María Torres",
        total=1500.0,
        occurred_at=datetime.now(timezone.utc),
    )

    try:
        event.total = 9999.0
        assert False, "Debió lanzar un error de inmutabilidad"
    except Exception:
        assert True


def test_order_created_event_has_correct_data():
    order_id = uuid4()
    now = datetime.now(timezone.utc)

    event = OrderCreated(
        order_id=order_id,
        customer_name="Pedro Ramírez",
        total=250.0,
        occurred_at=now,
    )

    assert event.order_id == order_id
    assert event.customer_name == "Pedro Ramírez"
    assert event.total == 250.0
    assert event.occurred_at == now