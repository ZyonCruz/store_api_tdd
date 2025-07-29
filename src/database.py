from motor.motor_asyncio import AsyncIOMotorClient
from src.settings import Settings

class MongoClient:
    """
    Classe para gerenciar a conexão com o MongoDB.
    """
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.settings = Settings()

    async def connect(self):
        """
        Estabelece a conexão com o cliente MongoDB.
        """
        if self.client is None:
            try:
                self.client = AsyncIOMotorClient(self.settings.DATABASE_URL)
                # O comando ping é uma forma leve de verificar a conexão
                await self.client.admin.command('ping')
                print("Conexão com MongoDB estabelecida com sucesso!")
            except Exception as e:
                print(f"Erro ao conectar ao MongoDB: {e}")
                # Re-levanta a exceção para que o erro seja propagado
                raise

    async def close(self):
        """
        Fecha a conexão com o cliente MongoDB.
        """
        if self.client:
            self.client.close()
            self.client = None
            print("Conexão com MongoDB fechada.")

    def get_database(self):
        """
        Retorna a instância do banco de dados.
        """
        if self.client is None:
            raise Exception("Cliente MongoDB não conectado. Chame connect() primeiro.")
        return self.client[self.settings.DB_NAME]

db_client = MongoClient()