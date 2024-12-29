#!/bin/bash
# Saia imediatamente se algum comando falhar
set -e

echo "Gerando novas migrações..."
python manage.py makemigrations  # Cria novas migrações com base nos modelos

echo "Iniciando migrações do banco de dados..."
python manage.py migrate  # Executa o migrate automaticamente

echo "Migrações concluídas. Iniciando o servidor Django..."
exec python manage.py runserver 0.0.0.0:8000  # Inicia o servidor Django
