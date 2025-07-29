import pytest
from src.schemas.product import ProductIn, ProductOut, ProductUpdate
from src.usecases.product import ProductUsecase
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

# Fixture para mockar o cliente MongoDB (não se conecta a um DB real)
@pytest.fixture
def mock_mongo_client(mocker):
    """
    Fixtura que retorna um mock do cliente MongoDB.
    Isso evita a necessidade de uma conexão real com o banco de dados para testes de usecase.
    """
    mock_collection = AsyncMock() # Usar AsyncMock diretamente para a coleção
    mock_db = MagicMock() # Usar MagicMock para o DB
    mock_db.get_collection.return_value = mock_collection
    mock_client = MagicMock() # Usar MagicMock para o cliente
    mock_client.get_database.return_value = mock_db
    return mock_client

# Fixture para o ProductUsecase
@pytest.fixture
def product_usecase(mock_mongo_client):
    """
    Fixtura que retorna uma instância do ProductUsecase para testes.
    Recebe o cliente MongoDB mockado.
    """
    usecase = ProductUsecase(client=mock_mongo_client)
    return usecase

# Helper para criar um mock de cursor assíncrono usando AsyncMock
def create_async_mock_cursor(data):
    """
    Cria um AsyncMock que se comporta como um cursor assíncrono para 'async for'.
    """
    mock_cursor = AsyncMock()
    # Configura o __aiter__ para retornar o próprio mock_cursor
    mock_cursor.__aiter__.return_value = mock_cursor
    # Configura o __anext__ para retornar os dados um por um e levantar StopAsyncIteration no final
    mock_cursor.__anext__.side_effect = data + [StopAsyncIteration]
    return mock_cursor


@pytest.mark.asyncio
async def test_create_product_usecase(product_usecase: ProductUsecase, product_in_data: dict, mocker):
    """
    Testa a criação de um produto através do usecase.
    """
    # Gerar um UUID para o produto que será "inserido"
    product_id = uuid4()

    # Mock do insert_one
    mocker.patch.object(product_usecase.collection, "insert_one", new_callable=AsyncMock, return_value=MagicMock(inserted_id=product_id))

    # Mock do find_one para a recuperação pós-criação
    # Garante que o _id no mock do DB é um UUID, para corresponder ao ProductOut
    mock_product_db = {
        "_id": product_id, # Usar o UUID gerado
        "name": product_in_data["name"],
        "quantity": product_in_data["quantity"],
        "price": product_in_data["price"],
        "created_at": datetime.now(), # Estes serão sobrescritos no ProductOut
        "updated_at": datetime.now(), # Estes serão sobrescritos no ProductOut
    }
    mocker.patch.object(product_usecase.collection, "find_one", new_callable=AsyncMock, return_value=mock_product_db)

    product_created = await product_usecase.create(body=ProductIn(**product_in_data))

    assert isinstance(product_created, ProductOut)
    assert product_created.id == product_id # Comparar com o UUID gerado
    assert product_created.name == product_in_data["name"]
    assert product_created.quantity == product_in_data["quantity"]
    assert product_created.price == product_in_data["price"]
    assert isinstance(product_created.created_at, datetime)
    assert isinstance(product_created.updated_at, datetime)

    product_usecase.collection.insert_one.assert_called_once()
    # A chamada a find_one é feita com o ID gerado internamente pelo usecase
    product_usecase.collection.find_one.assert_called_once_with({"_id": product_created.id})


@pytest.mark.asyncio
async def test_get_all_products_usecase(product_usecase: ProductUsecase, mocker):
    """
    Testa a listagem de todos os produtos através do usecase.
    """
    product1_db = {
        "_id": uuid4(), # Usar UUID
        "name": "Produto A", "quantity": 1, "price": 10.00,
        "created_at": datetime.now(), "updated_at": datetime.now()
    }
    product2_db = {
        "_id": uuid4(), # Usar UUID
        "name": "Produto B", "quantity": 2, "price": 20.00,
        "created_at": datetime.now(), "updated_at": datetime.now()
    }

    mock_products_data = [product1_db, product2_db]

    # Usar o helper para criar o mock de cursor
    mock_cursor_instance = create_async_mock_cursor(mock_products_data)
    mocker.patch.object(product_usecase.collection, "find", new_callable=AsyncMock, return_value=mock_cursor_instance)

    products = await product_usecase.get_all()

    assert len(products) == 2
    assert products[0].name == "Produto A"
    assert products[1].name == "Produto B"
    product_usecase.collection.find.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_by_id_usecase(product_usecase: ProductUsecase, mocker, product_in_data: dict):
    """
    Testa a busca de um produto por ID através do usecase.
    """
    product_id = uuid4() # Usar UUID
    mock_product_db = {
        "_id": product_id,
        "name": product_in_data["name"],
        "quantity": product_in_data["quantity"],
        "price": product_in_data["price"],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    mocker.patch.object(product_usecase.collection, "find_one", new_callable=AsyncMock, return_value=mock_product_db)

    product = await product_usecase.get_by_id(id=product_id)

    assert isinstance(product, ProductOut)
    assert product.id == product_id
    assert product.name == product_in_data["name"]
    product_usecase.collection.find_one.assert_called_once_with({"_id": product_id})

    # Teste para produto não encontrado
    mocker.patch.object(product_usecase.collection, "find_one", new_callable=AsyncMock, return_value=None)
    product = await product_usecase.get_by_id(id=uuid4()) # Usar um novo UUID para não encontrado
    assert product is None

@pytest.mark.asyncio
async def test_update_product_usecase(product_usecase: ProductUsecase, mocker, product_in_data: dict):
    """
    Testa a atualização de um produto através do usecase.
    """
    product_id = uuid4() # Usar UUID
    original_product_db = {
        "_id": product_id,
        "name": "Produto Original",
        "quantity": 10,
        "price": 100.00,
        "created_at": datetime.now() - timedelta(days=1),
        "updated_at": datetime.now() - timedelta(days=1),
    }
    updated_data = {"name": "Produto Atualizado", "price": 120.00}

    # Mock do find_one para simular que o produto existe antes da atualização
    mocker.patch.object(product_usecase.collection, "find_one", new_callable=AsyncMock, side_effect=[original_product_db, {**original_product_db, **updated_data, "updated_at": datetime.now()}])

    # Mock do update_one para simular a atualização no banco de dados
    mocker.patch.object(product_usecase.collection, "update_one", new_callable=AsyncMock, return_value=MagicMock(modified_count=1))

    product_update_in = ProductUpdate(**updated_data)
    updated_product = await product_usecase.update(id=product_id, body=product_update_in)

    assert isinstance(updated_product, ProductOut)
    assert updated_product.id == product_id
    assert updated_product.name == updated_data["name"]
    assert updated_product.price == updated_data["price"]
    assert updated_product.quantity == original_product_db["quantity"] # Quantidade não deve mudar
    assert updated_product.updated_at > original_product_db["updated_at"] # updated_at deve ser mais recente

    # Verifica se find_one foi chamado duas vezes
    assert product_usecase.collection.find_one.call_count == 2
    product_usecase.collection.update_one.assert_called_once()

    # Teste para produto não encontrado para atualização (re-mock find_one para retornar None)
    mocker.patch.object(product_usecase.collection, "find_one", new_callable=AsyncMock, return_value=None)
    product_not_found = await product_usecase.update(id=uuid4(), body=product_update_in) # Usar um novo UUID
    assert product_not_found is None


@pytest.mark.asyncio
async def test_delete_product_usecase(product_usecase: ProductUsecase, mocker):
    """
    Testa a deleção de um produto através do usecase.
    """
    product_id = uuid4() # Usar UUID

    # Mock do delete_one para simular a deleção no banco de dados
    # O usecase.delete não chama find_one antes de delete_one, ele apenas tenta deletar.
    mocker.patch.object(product_usecase.collection, "delete_one", new_callable=AsyncMock, return_value=MagicMock(deleted_count=1))

    result = await product_usecase.delete(id=product_id)

    assert result is True
    # Apenas assert delete_one foi chamado, pois find_one não é chamado no usecase.delete
    product_usecase.collection.delete_one.assert_called_once_with({"_id": product_id})

    # Teste para produto não encontrado para deleção (deleted_count=0)
    mocker.patch.object(product_usecase.collection, "delete_one", new_callable=AsyncMock, return_value=MagicMock(deleted_count=0))
    result_not_found = await product_usecase.delete(id=uuid4()) # Usar um novo UUID
    assert result_not_found is False

@pytest.mark.asyncio
async def test_get_products_by_price_range_usecase(product_usecase: ProductUsecase, mocker):
    """
    Testa a busca de produtos por faixa de preço através do usecase.
    """
    product1_db = {
        "_id": uuid4(), # Usar UUID
        "name": "Produto A", "quantity": 1, "price": 50.00,
        "created_at": datetime.now(), "updated_at": datetime.now()
    }
    product2_db = {
        "_id": uuid4(), # Usar UUID
        "name": "Produto B", "quantity": 2, "price": 150.00,
        "created_at": datetime.now(), "updated_at": datetime.now()
    }
    product3_db = {
        "_id": uuid4(), # Usar UUID
        "name": "Produto C", "quantity": 3, "price": 250.00,
        "created_at": datetime.now(), "updated_at": datetime.now()
    }

    mock_products_data = [product1_db, product2_db, product3_db]

    # Usar a classe AsyncMockCursor para criar o mock de cursor
    mock_cursor_instance = create_async_mock_cursor(mock_products_data)
    mocker.patch.object(product_usecase.collection, "find", new_callable=AsyncMock, return_value=mock_cursor_instance)

    # Teste com min_price e max_price
    products = await product_usecase.get_by_price_range(min_price=100, max_price=200)
    assert len(products) == 1
    assert products[0].name == "Produto B"
    product_usecase.collection.find.assert_called_once_with({"price": {"$gte": 100, "$lte": 200}})
    product_usecase.collection.find.reset_mock() # Resetar o mock para o próximo teste

    # Teste apenas com max_price
    products = await product_usecase.get_by_price_range(max_price=100)
    assert len(products) == 1
    assert products[0].name == "Produto A"
    product_usecase.collection.find.assert_called_once_with({"price": {"$lte": 100}})
    product_usecase.collection.find.reset_mock()

    # Teste apenas com min_price
    products = await product_usecase.get_by_price_range(min_price=200)
    assert len(products) == 1
    assert products[0].name == "Produto C"
    product_usecase.collection.find.assert_called_once_with({"price": {"$gte": 200}})
    product_usecase.collection.find.reset_mock()

    # Teste sem parâmetros (todos)
    products = await product_usecase.get_by_price_range()
    assert len(products) == 3
    product_usecase.collection.find.assert_called_once_with({})
    product_usecase.collection.find.reset_mock()