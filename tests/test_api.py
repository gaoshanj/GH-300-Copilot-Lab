import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_checksum_is_stable() -> None:
    first = client.post("/checksum", json={"text": "hello"})
    second = client.post("/checksum", json={"text": "hello"})
    assert first.status_code == 200
    assert first.json() == second.json()


def test_checksum_rejects_empty_text() -> None:
    response = client.post("/checksum", json={"text": ""})
    assert response.status_code == 422


def test_order_not_found() -> None:
    response = client.get("/orders/missing")
    assert response.status_code == 404


@pytest.mark.xfail(
    reason="Intentional lab defect; remove xfail after fixing summarize_order.",
    strict=True,
)
def test_order_total_includes_quantity() -> None:
    response = client.get("/orders/demo-100")
    assert response.status_code == 200
    assert response.json()["item_count"] == 3
    # This test exposes the intentional defect in app.service.summarize_order.
    assert response.json()["total"] == 28.00
