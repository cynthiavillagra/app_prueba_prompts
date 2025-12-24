# ============================================
# DOCKERFILE - Contenedor para despliegue
# ============================================
# Proyecto: CRUD Didáctico con Supabase
# Uso: docker build -t crud-notas . && docker run -p 8000:8000 crud-notas

FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cache de capas Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Puerto expuesto
EXPOSE 8000

# Comando de inicio (API server)
# Para CLI interactivo, usar: docker run -it crud-notas python main.py
CMD ["python", "api/index.py"]
