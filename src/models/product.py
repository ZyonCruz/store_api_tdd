from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field, UUID4
from bson import ObjectId
from datetime import datetime
from src.schemas.product import ProductIn # Importa o schema de entrada
from typing import Optional # Para campos opcionais

# Classe auxiliar para lidar com ObjectId do MongoDB no Pydantic
class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(type="string")

class ProductModel(ProductIn):
    """
    Modelo de dados para um produto no MongoDB.
    Herda de ProductIn e adiciona campos específicos do banco de dados.
    """
    id: UUID4 = Field(default_factory=UUID4, alias="_id") # Usa _id para compatibilidade com MongoDB
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        """
        Configurações adicionais para o Pydantic para este modelo.
        """
        populate_by_name = True # Permite que o Pydantic use o alias '_id' ao mapear
        arbitrary_types_allowed = True # Permite tipos arbitrários como ObjectId
        json_encoders = {ObjectId: str} # Converte ObjectId para string ao serializar
        from_attributes = True # Permite criar modelos a partir de objetos com atributos