from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from src.schemas.product import ProductIn, ProductOut, ProductUpdate
from src.core.exceptions import NotFoundException

class ProductUsecase:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.get_database().get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        # Gerar o UUID para o ID do produto
        product_id = uuid4()
        
        # Criar o objeto ProductOut com o ID gerado e timestamps
        product_out_data = {
            "id": product_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            **body.model_dump()
        }
        product = ProductOut(**product_out_data)
        
        # O MongoDB usa '_id' por padrão. Mapeamos o 'id' do Pydantic para '_id' no DB.
        # Ao usar product.model_dump(by_alias=True), o Pydantic já deveria fazer isso
        # se você configurou o alias corretamente no ProductOut.
        # No entanto, para garantir, vamos criar o dicionário para inserção explicitamente.
        db_product_data = product.model_dump(by_alias=True)
        db_product_data["_id"] = product_id # Garante que _id é o UUID

        await self.collection.insert_one(db_product_data)
        
        # Após a inserção, recuperamos o produto do banco de dados para garantir que todos os campos
        # gerados pelo DB (como _id) estejam presentes e corretos para a validação do ProductOut.
        # Usamos o ID que geramos para a busca.
        created_product_db = await self.collection.find_one({"_id": product_id})
        if not created_product_db:
            raise Exception("Product not found immediately after creation.")
        return ProductOut(**created_product_db)

    async def get_all(self) -> List[ProductOut]:
        products = []
        # O método .find() retorna um cursor.
        cursor = self.collection.find()
        async for product in cursor: # Iterar sobre o cursor retornado
            products.append(ProductOut(**product))
        return products

    async def get_by_id(self, id: UUID) -> Optional[ProductOut]:
        product = await self.collection.find_one({"_id": id})
        if not product:
            return None
        return ProductOut(**product)

    async def update(self, id: UUID, body: ProductUpdate) -> Optional[ProductOut]:
        product = await self.collection.find_one({"_id": id})
        if not product:
            return None

        update_data = body.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.now()

        # Garante que o ID não seja atualizado
        if "_id" in update_data:
            del update_data["_id"]

        await self.collection.update_one({"_id": id}, {"$set": update_data})

        # Recupera o documento atualizado para retornar
        updated_product = await self.collection.find_one({"_id": id})
        return ProductOut(**updated_product)

    async def delete(self, id: UUID) -> bool:
        # Primeiro, tenta deletar o produto.
        result = await self.collection.delete_one({"_id": id})
        return result.deleted_count > 0

    async def get_by_price_range(self, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[ProductOut]:
        query = {}
        if min_price is not None and max_price is not None:
            query["price"] = {"$gte": min_price, "$lte": max_price}
        elif min_price is not None:
            query["price"] = {"$gte": min_price}
        elif max_price is not None:
            query["price"] = {"$lte": max_price}

        products = []
        cursor = self.collection.find(query)
        async for product in cursor: # Iterar sobre o cursor retornado
            products.append(ProductOut(**product))
        return products