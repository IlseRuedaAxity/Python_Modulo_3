import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from orders.cli.main import app

runner = CliRunner()


def test_listar_sin_ordenes():
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    with patch("orders.cli.main.httpx.get", return_value=mock_response):
        result = runner.invoke(app, ["listar"])

    assert result.exit_code == 0
    assert "No hay órdenes registradas" in result.output


def test_listar_con_ordenes():
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "abc-123",
            "customer_name": "Ana García",
            "total": 1550.0,
            "status": "pending",
            "created_at": "2024-01-01T00:00:00",
        }
    ]
    mock_response.raise_for_status.return_value = None

    with patch("orders.cli.main.httpx.get", return_value=mock_response):
        result = runner.invoke(app, ["listar"])

    assert result.exit_code == 0
    assert "Ana García" in result.output
    assert "1550.00" in result.output