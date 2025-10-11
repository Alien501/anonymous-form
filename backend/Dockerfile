# Use Python 3.12 slim image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    grep -v "psycopg2" requirements.txt > requirements-no-postgres.txt && \
    pip install --no-cache-dir -r requirements-no-postgres.txt && \
    pip install --no-cache-dir gunicorn && \
    rm requirements-no-postgres.txt

COPY . .

RUN mkdir -p media/form_uploads

EXPOSE 8000

RUN chmod +x startup.sh

CMD ["./startup.sh"]

