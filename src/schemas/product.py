from pydantic import Field, UUID4
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchemaMixin

class ProductIn(BaseSchemaMixin):
    """
    Schema de entrada para criação de produtos.
    Define os campos necessários para criar um novo produto.
    """
    name: str = Field(..., description="Nome do produto")
    quantity: int = Field(..., description="Quantidade do produto em estoque")
    price: float = Field(..., description="Preço do produto")

class ProductOut(ProductIn):
    """
    Schema de saída para produtos.
    Inclui campos de ProductIn mais ID e timestamps.
    """
    id: UUID4 = Field(..., description="ID do produto")
    created_at: datetime = Field(..., description="Data de criação do produto")
    updated_at: datetime = Field(..., description="Data da última atualização do produto")

class ProductUpdate(BaseSchemaMixin):
    """
    Schema para atualização parcial de produtos.
    Todos os campos são opcionais.
    """
    name: Optional[str] = Field(None, description="Novo nome do produto")
    quantity: Optional[int] = Field(None, description="Nova quantidade do produto em estoque")
    price: Optional[float] = Field(None, description="Novo preço do produto")