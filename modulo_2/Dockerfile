# ─── Stage 1: Builder ───────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY orders/ orders/

RUN pip install --upgrade pip \
    && pip install build \
    && python -m build --wheel

# ─── Stage 2: Runtime ───────────────────────────────
FROM python:3.12-slim AS runtime

# Usuario sin privilegios root
RUN useradd --no-create-home --shell /bin/false appuser

WORKDIR /app

# Copiar solo el wheel desde el builder
COPY --from=builder /app/dist/*.whl .

# Instalar el paquete
RUN pip install --no-cache-dir *.whl \
    && rm *.whl

USER appuser

EXPOSE 8000

CMD ["uvicorn", "orders.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]