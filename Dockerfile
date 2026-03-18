# 1. Imagen base ligera
FROM python:3.11-slim

# 2. Configurar variables de entorno para evitar archivos .pyc y forzar logs en consola
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Establecer el directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias del sistema (necesarias para algunas librerías de red o bases de datos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código de la aplicación
COPY . .

# 7. Exponer el puerto que usará FastAPI (por defecto 8000)
EXPOSE 8000

# 8. Comando para iniciar la aplicación con Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]