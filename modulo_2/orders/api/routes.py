from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orders.application.use_cases import CreateOrder, ListOrders, DeleteOrder
from orders.infrastructure.repository_memory import InMemoryUnitOfWork
from orders.infrastructure.event_handler import handle_order_created


app = FastAPI(
    title="Orders API",
    description="Servicio de Orders con Arquitectura Limpia",
    version="0.1.0",
)

# Repositorio compartido en memoria
_uow = InMemoryUnitOfWork()


class OrderItemRequest(BaseModel):
    product_name: str
    quantity: int
    unit_price: float


class CreateOrderRequest(BaseModel):
    customer_name: str
    items: list[OrderItemRequest]


@app.get("/orders", summary="Listar todas las órdenes")
def list_orders():
    use_case = ListOrders(uow=_uow)
    return use_case.execute()


@app.post("/orders", status_code=201, summary="Crear una nueva orden")
def create_order(request: CreateOrderRequest):
    use_case = CreateOrder(uow=_uow, event_handler=handle_order_created)
    return use_case.execute(
        customer_name=request.customer_name,
        items_data=[item.model_dump() for item in request.items],
    )


@app.delete("/orders/{order_id}", status_code=204, summary="Eliminar una orden")
def delete_order(order_id: str):
    use_case = DeleteOrder(uow=_uow)
    deleted = use_case.execute(order_id=order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Orden no encontrada")