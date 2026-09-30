import grpc
import uuid
import time
from concurrent import futures

from app.orders import orders_pb2, orders_pb2_grpc


# ── Almacenamiento en memoria ─────────────────────────────
orders_db: dict = {}


# ── Implementación del servicio ───────────────────────────
class OrderServiceServicer(orders_pb2_grpc.OrderServiceServicer):

    def CreateOrder(self, request, context):
        # Calcular total
        total = sum(item.price * item.quantity for item in request.items)

        # Crear orden
        order_id = str(uuid.uuid4())
        order = {
            "order_id": order_id,
            "customer_id": request.customer_id,
            "status": "created",
            "total": total,
        }
        orders_db[order_id] = order

        print(f"[SERVER] Orden creada: {order_id} - Total: {total}")

        return orders_pb2.OrderResponse(
            order_id=order_id,
            customer_id=request.customer_id,
            status="created",
            total=total,
        )

    def GetOrder(self, request, context):
        order = orders_db.get(request.order_id)

        if not order:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Orden {request.order_id} no encontrada")
            return orders_pb2.OrderResponse()

        return orders_pb2.OrderResponse(**order)

    def ListOrders(self, request, context):
        all_orders = [
            orders_pb2.OrderResponse(**o) for o in orders_db.values()
        ]
        return orders_pb2.OrderListResponse(orders=all_orders)


# ── Iniciar servidor ──────────────────────────────────────
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(
        OrderServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("[SERVER] Servidor gRPC corriendo en puerto 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("[SERVER] Servidor detenido.")


if __name__ == "__main__":
    serve()