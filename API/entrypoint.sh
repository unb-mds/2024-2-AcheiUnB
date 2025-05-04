#!/bin/bash
# Saia imediatamente se algum comando falhar
set -e

echo "Executando Black para formatar o código..."
black .  

echo "Executando Ruff para verificar a formatação do código..."
ruff . --fix

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Gerando novas migrações..."
    python manage.py makemigrations --noinput  

    echo "Aplicando migrações ao banco de dados..."
    python manage.py migrate --noinput  

    echo "Migrações concluídas."
else
    echo "Não executando migrações neste serviço."
fi

# Executa o comando recebido
exec "$@"
