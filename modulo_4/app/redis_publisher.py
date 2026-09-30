import redis
import json
import uuid
from datetime import datetime, UTC


# ── Conectar a Redis ──────────────────────────────────────
def get_redis_client():
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )


# ── Evento OrderCreated ───────────────────────────────────
def publish_order_created(order_id: str, customer_id: str, total: float):
    client = get_redis_client()

    event = {
        "event_type": "OrderCreated",
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "order_id": order_id,
            "customer_id": customer_id,
            "total": total,
            "status": "created",
        },
    }

    # Publicar en canal Redis
    channel = "orders.events"
    message = json.dumps(event)
    client.publish(channel, message)

    print(f"[REDIS] Evento publicado en '{channel}':")
    print(json.dumps(event, indent=2))


# ── Suscriptor para escuchar eventos ─────────────────────
def subscribe_orders():
    client = get_redis_client()
    pubsub = client.pubsub()
    pubsub.subscribe("orders.events")

    print("[REDIS] Escuchando eventos en 'orders.events'...")
    for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"])
            print(f"\n[REDIS] Evento recibido:")
            print(json.dumps(event, indent=2))


if __name__ == "__main__":
    publish_order_created(
        order_id=str(uuid.uuid4()),
        customer_id="cliente-001",
        total=61.00,
    )