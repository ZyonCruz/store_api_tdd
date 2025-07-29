from fastapi import FastAPI
from src.controllers.product import product_controller
from src.database import db_client

# Cria uma instância da aplicação FastAPI
app = FastAPI(title="Store API", version="0.1.0")

# Inclui o roteador de produtos na aplicação
app.include_router(product_controller)

@app.on_event("startup")
async def startup_event():
    """
    Evento de inicialização da aplicação.
    Conecta ao banco de dados MongoDB.
    """
    await db_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento de desligamento da aplicação.
    Fecha a conexão com o banco de dados MongoDB.
    """
    await db_client.close()

@app.get("/")
async def read_root():
    """
    Endpoint raiz para verificar o status da API.
    """
    return {"message": "Welcome to the Store API!"}