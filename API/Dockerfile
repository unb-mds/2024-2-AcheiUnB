FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /var/log/django

COPY . /app/

EXPOSE 8080

COPY --chmod=755 entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "AcheiUnB.wsgi:application"]