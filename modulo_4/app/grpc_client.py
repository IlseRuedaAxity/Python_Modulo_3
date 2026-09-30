import grpc
from app.orders import orders_pb2, orders_pb2_grpc


def run():
    # ── Conectar al servidor gRPC ─────────────────────────
    channel = grpc.insecure_channel("localhost:50051")
    stub = orders_pb2_grpc.OrderServiceStub(channel)

    print("=" * 50)
    print("🧪 TEST 1 — Crear una orden")
    print("=" * 50)

    # ── Crear orden ───────────────────────────────────────
    request = orders_pb2.CreateOrderRequest(
        customer_id="cliente-001",
        items=[
            orders_pb2.OrderItem(product_id="prod-1", quantity=2, price=15.50),
            orders_pb2.OrderItem(product_id="prod-2", quantity=1, price=30.00),
        ],
    )

    response = stub.CreateOrder(request)
    print(f"✅ Orden creada:")
    print(f"   ID:         {response.order_id}")
    print(f"   Cliente:    {response.customer_id}")
    print(f"   Status:     {response.status}")
    print(f"   Total:      ${response.total:.2f}")

    print()
    print("=" * 50)
    print("🧪 TEST 2 — Obtener la orden creada")
    print("=" * 50)

    # ── Obtener orden ─────────────────────────────────────
    get_request = orders_pb2.GetOrderRequest(order_id=response.order_id)
    get_response = stub.GetOrder(get_request)
    print(f"✅ Orden encontrada:")
    print(f"   ID:         {get_response.order_id}")
    print(f"   Status:     {get_response.status}")
    print(f"   Total:      ${get_response.total:.2f}")

    print()
    print("=" * 50)
    print("🧪 TEST 3 — Listar todas las órdenes")
    print("=" * 50)

    # ── Listar órdenes ────────────────────────────────────
    list_request = orders_pb2.GetOrderRequest(order_id="")
    list_response = stub.ListOrders(list_request)
    print(f"✅ Total de órdenes: {len(list_response.orders)}")
    for order in list_response.orders:
        print(f"   - {order.order_id} | {order.customer_id} | ${order.total:.2f}")


if __name__ == "__main__":
    run()