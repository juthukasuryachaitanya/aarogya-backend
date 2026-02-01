FROM python:3.11-slim

# ==========================
# SYSTEM SETTINGS
# ==========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend

WORKDIR /backend

# ==========================
# SYSTEM DEPENDENCIES
# ==========================
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# PYTHON DEPENDENCIES
# ==========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# APP CODE
# ==========================
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# ==========================
# SECURITY: NON-ROOT USER
# ==========================
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# ==========================
# NETWORK
# ==========================
EXPOSE 8000

# ==========================
# START SERVER
# ==========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
