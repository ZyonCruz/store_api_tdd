# Usa uma imagem base oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . .

# Expõe a porta em que a aplicação FastAPI será executada
EXPOSE 8000

# Comando para iniciar a aplicação Uvicorn
# --host 0.0.0.0 permite que a aplicação seja acessível de fora do container
# --port 8000 especifica a porta
# src.main:app indica que a aplicação está no arquivo src/main.py e a instância é 'app'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]