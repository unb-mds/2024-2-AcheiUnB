# Use a imagem oficial do Python
FROM python:3.12

# Define o diretório de trabalho
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

# Copia o arquivo de dependências
COPY requirements.txt /app/

# Atualize o pip antes de instalar os requisitos
RUN python -m pip install --upgrade pip

# Instala as dependencias do Heroku
RUN pip install dj-database-url psycopg2-binary

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para dentro do container
COPY . /app/

# Copia o entrypoint.sh e define como executável

COPY --chmod=755 entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exponha a porta que o Django usará
EXPOSE 8000

# Use o entrypoint.sh como ponto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Instala o Gunicorn
RUN pip install gunicorn

# Exponha a porta usada pelo Django
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["gunicorn", "AcheiUnB.wsgi:application", "--bind", "0.0.0.0:8000"]