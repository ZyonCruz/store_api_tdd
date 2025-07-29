import pymongo
from pymongo.errors import ServerSelectionTimeoutError

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Conexão com o MongoDB bem-sucedida!")
    # Tente listar as bases de dados para uma verificação mais completa
    print("Bases de dados existentes:", client.list_database_names())
except ServerSelectionTimeoutError as err:
    print(f"Erro de conexão com o MongoDB: {err}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
finally:
    if 'client' in locals() and client:
        client.close()