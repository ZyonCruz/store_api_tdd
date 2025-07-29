import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from src.schemas.product import ProductIn, ProductOut # Importa ProductIn e ProductOut

def test_product_in_schema():
    """
    Testa a criação de um schema ProductIn com dados válidos.
    Verifica se os dados são atribuídos corretamente.
    """
    data = {
        "name": "Produto Teste",
        "quantity": 10,
        "price": 100.50,
    }
    product = ProductIn(**data)

    assert product.name == "Produto Teste"
    assert product.quantity == 10
    assert product.price == 100.50

def test_product_in_schema_invalid_data():
    """
    Testa a validação de um schema ProductIn com dados inválidos.
    Esperar que uma ValidationError seja levantada para dados incorretos.
    """
    with pytest.raises(ValidationError):
        # 'dez' é um valor inválido para o campo 'quantity', que esperamos ser um número.
        ProductIn(name="Produto Teste", quantity="dez", price=100.50)

def test_product_out_schema():
    """
    Testa a criação de um schema ProductOut com dados válidos, incluindo os campos do BaseSchema.
    """
    data = {
        "id": str(uuid4()), # ID gerado para o teste
        "name": "Produto Teste Out",
        "quantity": 5,
        "price": 200.00,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    product_out = ProductOut(**data)

    assert product_out.name == "Produto Teste Out"
    assert product_out.quantity == 5
    assert product_out.price == 200.00
    assert isinstance(product_out.id, uuid4().__class__) # Verifica se o tipo do ID é UUID
    assert isinstance(product_out.created_at, datetime)
    assert isinstance(product_out.updated_at, datetime)