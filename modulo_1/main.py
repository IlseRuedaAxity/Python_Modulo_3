from application.use_cases import CreateOrder
from infrastructure.repository_memory import InMemoryUnitOfWork
from infrastructure.event_handler import handle_order_created
import json


def main():
    uow = InMemoryUnitOfWork()
    use_case = CreateOrder(uow=uow, event_handler=handle_order_created)

    print("=" * 50)
    print("Creando Order #1...")
    result = use_case.execute(
        customer_name="María Torres",
        items_data=[
            {"product_name": "Laptop",  "quantity": 1, "unit_price": 1200.0},
            {"product_name": "Mochila", "quantity": 1, "unit_price": 45.0},
        ],
    )
    print("\nResultado (via Presenter):")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    print("\n" + "=" * 50)
    print("Creando Order #2...")
    result2 = use_case.execute(
        customer_name="Carlos López",
        items_data=[
            {"product_name": "Monitor", "quantity": 2, "unit_price": 300.0},
            {"product_name": "Teclado", "quantity": 1, "unit_price": 80.0},
        ],
    )
    print("\nResultado (via Presenter):")
    print(json.dumps(result2, indent=2, ensure_ascii=False))

    print("\n" + "=" * 50)
    print(f"Total orders en repositorio: {len(uow.orders.list_all())}")


if __name__ == "__main__":
    main()