import typer
import httpx
import json

app = typer.Typer(help="CLI para gestionar Orders")

BASE_URL = "http://localhost:8000"


@app.command()
def listar():
    """Lista todas las órdenes."""
    try:
        response = httpx.get(f"{BASE_URL}/orders")
        response.raise_for_status()
        orders = response.json()

        if not orders:
            typer.echo("No hay órdenes registradas.")
            return

        for order in orders:
            typer.echo("-" * 40)
            typer.echo(f"ID       : {order['id']}")
            typer.echo(f"Cliente  : {order['customer_name']}")
            typer.echo(f"Total    : ${order['total']:.2f}")
            typer.echo(f"Status   : {order['status']}")
            typer.echo(f"Creado   : {order['created_at']}")

    except httpx.ConnectError:
        typer.echo("❌ Error: No se puede conectar a la API. ¿Está corriendo?")
        raise typer.Exit(code=1)


@app.command()
def crear(
    cliente: str = typer.Option(..., prompt="Nombre del cliente"),
    producto: str = typer.Option(..., prompt="Nombre del producto"),
    cantidad: int = typer.Option(..., prompt="Cantidad"),
    precio: float = typer.Option(..., prompt="Precio unitario"),
):
    """Crea una nueva orden."""
    try:
        payload = {
            "customer_name": cliente,
            "items": [
                {
                    "product_name": producto,
                    "quantity": cantidad,
                    "unit_price": precio,
                }
            ],
        }
        response = httpx.post(f"{BASE_URL}/orders", json=payload)
        response.raise_for_status()
        order = response.json()

        typer.echo("\n✅ Orden creada exitosamente!")
        typer.echo(f"ID       : {order['id']}")
        typer.echo(f"Cliente  : {order['customer_name']}")
        typer.echo(f"Total    : ${order['total']:.2f}")

    except httpx.ConnectError:
        typer.echo("❌ Error: No se puede conectar a la API. ¿Está corriendo?")
        raise typer.Exit(code=1)


@app.command()
def borrar(
    order_id: str = typer.Option(..., prompt="ID de la orden a borrar"),
):
    """Borra una orden por ID."""
    try:
        response = httpx.delete(f"{BASE_URL}/orders/{order_id}")

        if response.status_code == 204:
            typer.echo(f"✅ Orden {order_id} eliminada correctamente.")
        elif response.status_code == 404:
            typer.echo(f"❌ Orden {order_id} no encontrada.")
        else:
            typer.echo(f"❌ Error inesperado: {response.status_code}")

    except httpx.ConnectError:
        typer.echo("❌ Error: No se puede conectar a la API. ¿Está corriendo?")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()