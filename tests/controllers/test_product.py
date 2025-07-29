import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.schemas.product import ProductIn, ProductOut, ProductUpdate
from uuid import UUID
from datetime import datetime, timedelta

# Fixture para o cliente de teste FastAPI
@pytest.fixture
def client():
    """
    Fixtura que fornece um cliente de teste síncrono para testar os endpoints da API.
    """
    with TestClient(app=app) as client:
        yield client

# As fixtures product_in_data e product_update_data foram movidas para conftest.py
# Elas serão injetadas automaticamente pelo pytest.

def test_post_product(client: TestClient, product_in_data: dict, clear_database):
    """
    Testa o endpoint POST /products para criar um novo produto.
    """
    response = client.post("/products", json=product_in_data)
    assert response.status_code == 201
    
    response_json = response.json()
    assert "id" in response_json
    product_id_from_response = UUID(response_json["id"])

    product_out = ProductOut(**response_json)
    
    assert product_out.id == product_id_from_response
    assert product_out.name == product_in_data["name"]
    assert product_out.quantity == product_in_data["quantity"]
    assert product_out.price == product_in_data["price"]
    assert isinstance(product_out.created_at, datetime)
    assert isinstance(product_out.updated_at, datetime)

def test_get_all_products(client: TestClient, product_in_data: dict, clear_database):
    """
    Testa o endpoint GET /products para listar todos os produtos.
    """
    client.post("/products", json=product_in_data)
    client.post("/products", json={**product_in_data, "name": "Tablet", "price": 500.00})

    response = client.get("/products")
    assert response.status_code == 200
    products = [ProductOut(**p) for p in response.json()]
    assert len(products) == 2
    assert any(p.name == "Smartphone" for p in products)
    assert any(p.name == "Tablet" for p in products)

def test_get_product_by_id(client: TestClient, product_in_data: dict, clear_database):
    """
    Testa o endpoint GET /products/{id} para buscar um produto por ID.
    """
    post_response = client.post("/products", json=product_in_data)
    product_id_str = post_response.json()["id"]

    get_response = client.get(f"/products/{product_id_str}")
    assert get_response.status_code == 200
    product_out = ProductOut(**get_response.json())
    assert str(product_out.id) == product_id_str
    assert product_out.name == product_in_data["name"]

    not_found_id = UUID("a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d")
    not_found_response = client.get(f"/products/{not_found_id}")
    assert not_found_response.status_code == 404
    assert not_found_response.json()["detail"] == f"Product not found with id: {not_found_id}"

def test_patch_product(client: TestClient, product_in_data: dict, product_update_data: dict, clear_database):
    """
    Testa o endpoint PATCH /products/{id} para atualizar um produto.
    """
    post_response = client.post("/products", json=product_in_data)
    product_id_str = post_response.json()["id"]

    patch_response = client.patch(f"/products/{product_id_str}", json=product_update_data)
    assert patch_response.status_code == 200
    updated_product = ProductOut(**patch_response.json())
    assert str(updated_product.id) == product_id_str
    assert updated_product.name == product_update_data["name"]
    assert updated_product.price == product_update_data["price"]
    assert updated_product.quantity == product_in_data["quantity"]

    not_found_id = UUID("a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6e")
    not_found_response = client.patch(f"/products/{not_found_id}", json=product_update_data)
    assert not_found_response.status_code == 404
    assert not_found_response.json()["detail"] == f"Product not found with id: {not_found_id}"

def test_delete_product(client: TestClient, product_in_data: dict, clear_database):
    """
    Testa o endpoint DELETE /products/{id} para deletar um produto.
    """
    post_response = client.post("/products", json=product_in_data)
    product_id_str = post_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id_str}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/products/{product_id_str}")
    assert get_response.status_code == 404

    not_found_id = UUID("a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6f")
    not_found_response = client.delete(f"/products/{not_found_id}")
    assert not_found_response.status_code == 404
    assert not_found_response.json()["detail"] == f"Product not found with id: {not_found_id}"

def test_post_product_exception(client: TestClient, product_in_data: dict, mocker, clear_database):
    """
    Testa o endpoint POST /products para garantir que exceções são tratadas.
    """
    mocker.patch("src.usecases.product.ProductUsecase.create", side_effect=Exception("Database error"))

    response = client.post("/products", json=product_in_data)
    assert response.status_code == 500
    assert response.json()["detail"] == "Database error"

def test_get_products_by_price_range(client: TestClient, product_in_data: dict, clear_database):
    """
    Testa o endpoint GET /products/price_range para buscar produtos por faixa de preço.
    """
    client.post("/products", json={**product_in_data, "name": "Produto Barato", "price": 50.00})
    client.post("/products", json={**product_in_data, "name": "Produto Medio", "price": 150.00})
    client.post("/products", json={**product_in_data, "name": "Produto Caro", "price": 250.00})

    response = client.get("/products/price_range?min_price=100&max_price=200")
    assert response.status_code == 200
    products = [ProductOut(**p) for p in response.json()]
    assert len(products) == 1
    assert products[0].name == "Produto Medio"

    response = client.get("/products/price_range?max_price=100")
    assert response.status_code == 200
    products = [ProductOut(**p) for p in response.json()]
    assert len(products) == 1
    assert products[0].name == "Produto Barato"

    response = client.get("/products/price_range?min_price=200")
    assert response.status_code == 200
    products = [ProductOut(**p) for p in response.json()]
    assert len(products) == 1
    assert products[0].name == "Produto Caro"

    response = client.get("/products/price_range")
    assert response.status_code == 200
    products = [ProductOut(**p) for p in response.json()]
    assert len(products) == 3