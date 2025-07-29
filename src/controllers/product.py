from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Optional
from uuid import UUID

from src.schemas.product import ProductIn, ProductOut, ProductUpdate
from src.usecases.product import ProductUsecase
from src.database import db_client
from src.core.exceptions import NotFoundException

# Cria um roteador de API para os endpoints de produto
product_controller = APIRouter(prefix="/products", tags=["products"])

# Dependência para obter a instância do usecase de produto
def get_product_usecase() -> ProductUsecase:
    """
    Retorna uma instância de ProductUsecase com o cliente de banco de dados.
    """
    return ProductUsecase(client=db_client.client)

@product_controller.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo produto"
)
async def create_product(
    product_in: ProductIn,
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Cria um novo produto com base nos dados fornecidos.

    - **name**: Nome do produto (string)
    - **quantity**: Quantidade em estoque (inteiro)
    - **price**: Preço do produto (float)

    Retorna o produto criado, incluindo seu ID e timestamps.
    """
    try:
        product = await usecase.create(body=product_in)
        return product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@product_controller.get(
    "/",
    response_model=List[ProductOut],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os produtos"
)
async def get_all_products(
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Retorna uma lista de todos os produtos cadastrados.
    """
    products = await usecase.get_all()
    return products

@product_controller.get(
    "/{id}",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK,
    summary="Busca um produto pelo ID"
)
async def get_product_by_id(
    id: UUID,
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Busca um produto específico pelo seu ID.

    - **id**: ID do produto (UUID)

    Retorna o produto encontrado.
    Levanta um erro 404 se o produto não for encontrado.
    """
    product = await usecase.get_by_id(id=id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
    return product

@product_controller.patch(
    "/{id}",
    response_model=ProductOut,
    status_code=status.HTTP_200_OK,
    summary="Atualiza um produto pelo ID"
)
async def update_product(
    id: UUID,
    product_update: ProductUpdate,
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Atualiza parcialmente um produto existente pelo seu ID.

    - **id**: ID do produto a ser atualizado (UUID)
    - **product_update**: Dados para atualização (ProductUpdate, campos opcionais)

    Retorna o produto atualizado.
    Levanta um erro 404 se o produto não for encontrado.
    """
    updated_product = await usecase.update(id=id, body=product_update)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
    return updated_product

@product_controller.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um produto pelo ID"
)
async def delete_product(
    id: UUID,
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Deleta um produto existente pelo seu ID.

    - **id**: ID do produto a ser deletado (UUID)

    Retorna um status 204 (No Content) se a deleção for bem-sucedida.
    Levanta um erro 404 se o produto não for encontrado.
    """
    deleted = await usecase.delete(id=id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
    return

@product_controller.get(
    "/price_range",
    response_model=List[ProductOut],
    status_code=status.HTTP_200_OK,
    summary="Lista produtos por faixa de preço"
)
async def get_products_by_price_range(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    usecase: ProductUsecase = Depends(get_product_usecase)
):
    """
    Retorna uma lista de produtos dentro de uma faixa de preço especificada.

    - **min_price**: Preço mínimo (opcional)
    - **max_price**: Preço máximo (opcional)
    """
    products = await usecase.get_by_price_range(min_price=min_price, max_price=max_price)
    return products