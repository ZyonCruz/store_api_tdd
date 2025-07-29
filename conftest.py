import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from src.settings import Settings
from src.database import db_client # Importa a instância global db_client do seu database.py
from uuid import UUID
from datetime import datetime, timedelta

settings = Settings()

@pytest.fixture(scope="session", autouse=True)
async def mongo_client_fixture():
    """
    Fixtura que gerencia a conexão com o cliente MongoDB para a sessão de testes.
    'autouse=True' garante que esta fixture seja executada automaticamente uma vez por sessão.
    """
    db_client.client = AsyncIOMotorClient(settings.DATABASE_URL)
    try:
        await db_client.client.admin.command('ping')
        print("Conexão com MongoDB estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        raise # Re-levanta a exceção para que o erro seja propagada

    yield db_client.client
    db_client.client.close()
    print("Conexão com MongoDB fechada.")

@pytest.fixture(scope="function")
async def clear_database(mongo_client_fixture: AsyncIOMotorClient):
    """
    Fixtura que limpa todas as coleções do banco de dados de teste antes de cada função de teste.
    Isso garante que os testes sejam isolados e não interfiram uns nos outros.
    """
    db = mongo_client_fixture[settings.DB_NAME]
    for collection_name in await db.list_collection_names():
        if collection_name.startswith("system."):
            continue
        await db.drop_collection(collection_name)

# Fixture para dados de produto de entrada (agora em conftest.py)
@pytest.fixture
def product_in_data():
    """
    Fixtura que fornece dados de exemplo para um ProductIn.
    """
    return {
        "name": "Smartphone",
        "quantity": 10,
        "price": 999.99
    }

# Fixture para dados de atualização de produto (agora em conftest.py)
@pytest.fixture
def product_update_data():
    """
    Fixtura que fornece dados de exemplo para um ProductUpdate.
    """
    return {
        "name": "Smartphone Pro",
        "price": 1099.99
    }