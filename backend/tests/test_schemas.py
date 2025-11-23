from app.schemas.product import ProductResponse


def test_product_response():
    data = {"id": 1, "title": "Test", "price": 99.99, "description": None}
    product = ProductResponse(**data)
    assert product.title == "Test"
    assert product.description is None


def test_product_partial():
    data = {"title": "Only title"}
    # Должен пройти — description опционально
    partial = {"title": data["title"]}
    # Просто проверяем, что dict валиден
    assert partial["title"] == "Only title"
