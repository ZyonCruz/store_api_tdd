Store API TDD (FastAPI + MongoDB)
Este projeto implementa uma API RESTful para gerenciamento de produtos em uma loja, seguindo uma abordagem de Desenvolvimento Orientado a Testes (TDD). A API permite operações CRUD (Criar, Ler, Atualizar, Deletar) para produtos, além de funcionalidades de busca por faixa de preço.

🚀 Funcionalidades
Criação de Produtos: Adiciona novos produtos ao estoque.

Listagem de Produtos: Retorna todos os produtos cadastrados.

Busca por ID: Permite buscar um produto específico pelo seu identificador único (UUID).

Atualização de Produtos: Atualiza informações de produtos existentes (parcial ou completa).

Deleção de Produtos: Remove produtos do estoque.

Busca por Faixa de Preço: Filtra produtos com base em um intervalo de preços.

🛠️ Tecnologias Utilizadas
Python 3.12+

FastAPI: Framework web moderno e rápido para construir APIs com Python.

Pydantic: Para validação de dados e serialização/deserialização de modelos.

Motor: Driver MongoDB assíncrono para Python.

MongoDB: Banco de dados NoSQL para persistência de dados.

Docker & Docker Compose: Para orquestração e gerenciamento de contêineres (aplicação e banco de dados).

Pytest: Framework de testes para Python.

pytest-asyncio, pytest-mock: Plugins para testes assíncronos e mocks.

📁 Estrutura do Projeto
store_api_tdd/
├── .env                      # Variáveis de ambiente (credenciais, URLs)
├── .gitignore                # Arquivos a serem ignorados pelo Git
├── Dockerfile                # Definição da imagem Docker da aplicação
├── docker-compose.yml        # Orquestração dos serviços (API e MongoDB)
├── pytest.ini                # Configurações do Pytest
├── conftest.py               # Fixtures e configurações globais para testes
├── requirements.txt          # Dependências do Python
├── src/                      # Código fonte da aplicação
│   ├── __init__.py
│   ├── main.py               # Ponto de entrada da aplicação FastAPI
│   ├── settings.py           # Configurações da aplicação
│   ├── database.py           # Configuração da conexão com o MongoDB
│   ├── controllers/          # Camada de controle (endpoints da API)
│   │   ├── __init__.py
│   │   └── product.py
│   ├── usecases/             # Camada de lógica de negócio (regras de negócio)
│   │   ├── __init__.py
│   │   └── product.py
│   ├── schemas/              # Camada de validação de dados (Pydantic models)
│   │   ├── __init__.py
│   │   ├── base.py           # Mixin base para schemas Pydantic
│   │   └── product.py
│   └── core/                 # Componentes centrais (ex: exceções customizadas)
│       ├── __init__.py
│       └── exceptions.py
├── tests/                    # Testes da aplicação
│   ├── __init__.py
│   ├── controllers/
│   │   └── test_product.py   # Testes dos endpoints da API
│   ├── schemas/
│   │   └── test_product.py   # Testes dos modelos Pydantic
│   └── usecases/
│       └── test_product.py   # Testes da lógica de negócio
└── README.md                 # Este arquivo!

🚀 Como Começar
Siga estas instruções para configurar e rodar o projeto em sua máquina local.

Pré-requisitos
Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

Docker Desktop

Instalação e Execução
Clone o repositório:

git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO # Substitua pelo nome do seu repositório

Crie o arquivo de variáveis de ambiente .env:
No diretório raiz do projeto, crie um arquivo chamado .env e adicione as seguintes variáveis, substituindo os valores pelos que você deseja usar para o seu banco de dados MongoDB:

MONGO_INITDB_ROOT_USERNAME=your_mongo_username
MONGO_INITDB_ROOT_PASSWORD=your_mongo_password
DATABASE_URL=mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@mongodb:27017/
DB_NAME=store_api_test

Construa e inicie os serviços Docker:
Este comando irá construir a imagem da sua aplicação e iniciar os contêineres do FastAPI e do MongoDB.

docker-compose up -d --build

Aguarde alguns segundos para que os serviços estejam totalmente operacionais. Você pode verificar o status dos contêineres com docker ps.

Acesse a API:
A API estará disponível em http://localhost:8000.
A documentação interativa (Swagger UI) estará em http://localhost:8000/docs.
A documentação alternativa (ReDoc) estará em http://localhost:8000/redoc.

Parando os Serviços
Para parar e remover os contêineres, execute:

docker-compose down

Para uma limpeza completa (remover volumes e imagens também), use:

docker-compose down --volumes --rmi all

🧪 Rodando os Testes
Para rodar os testes, você pode usar o pytest dentro do seu ambiente virtual Python.

Ative seu ambiente virtual:

# Exemplo para Windows PowerShell
& ./.venv/Scripts/Activate.ps1
# Exemplo para Linux/macOS
source ./.venv/bin/activate

Instale as dependências (se ainda não o fez):

pip install -r requirements.txt

Execute o Pytest:

pytest

⚠️ Problemas Conhecidos
Durante o desenvolvimento e execução dos testes em alguns ambientes, pode ocorrer um erro de conexão com o MongoDB:

pymongo.errors.ServerSelectionTimeoutError: mongodb:27017: [Errno 11001] getaddrinfo failed

Este erro indica que o serviço da aplicação não conseguiu estabelecer uma conexão com o contêiner do MongoDB. As causas comuns incluem:

Problemas de rede ou DNS no ambiente Docker.

Configurações de firewall.

O contêiner do MongoDB não está totalmente inicializado ou acessível.

Inconsistências na instalação do Docker.

Este problema é de ambiente/infraestrutura e não um erro no código da aplicação. Assegure-se de que o Docker está funcionando corretamente e que não há conflitos de porta.

🤝 Contribuindo
Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma ideia para uma nova funcionalidade, sinta-se à vontade para abrir uma issue ou enviar um pull request.