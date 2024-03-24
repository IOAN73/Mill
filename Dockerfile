FROM python:3.11 AS builder

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python -m pip install --no-cache-dir poetry==1.8.1 \
    && poetry config virtualenvs.in-project true \
    && poetry install

FROM python:3.11-slim

COPY --from=builder /app /app
COPY server/ ./server/

CMD ["/app/.venv/bin/uvicorn", "server.main:app", "--host", "0.0.0.0"]
