# ── Etapa 1: builder ──────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ── Etapa 2: runtime ──────────────────────────────────────
FROM python:3.12-slim AS runtime

# ✅ Crear usuario sin privilegios
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# Copiar dependencias desde builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código
COPY ./app ./app
COPY .env.example .env

# ✅ Permisos mínimos
RUN chown -R appuser:appgroup /app \
    && chmod -R 550 /app \
    && chmod 440 /app/.env

# ✅ Cambiar a usuario sin root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]