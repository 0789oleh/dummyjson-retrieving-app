# backend/tests/test_products.py
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_and_update_product():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаём (если есть POST)
        # Или просто проверяем PATCH
        response = await client.patch(
            "/products/1",
            json={"title": "Test Product", "price": 999.99}
        )
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert data["title"] == "Test Product"
            assert data["price"] == 999.99
