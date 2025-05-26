FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir gunicorn

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

WORKDIR /app