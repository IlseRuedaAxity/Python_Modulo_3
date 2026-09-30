from orders.domain.events import OrderCreated


def handle_order_created(event: OrderCreated) -> None:
    """
    Manejador del evento OrderCreated.
    En producción aquí podrías enviar un email,
    notificar a un broker, etc.
    """
    print(f"[EVENT] OrderCreated disparado!")
    print(f"  → Order ID  : {event.order_id}")
    print(f"  → Cliente   : {event.customer_name}")
    print(f"  → Total     : ${event.total:.2f}")
    print(f"  → Timestamp : {event.occurred_at}")