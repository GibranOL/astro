# Usamos una imagen oficial de Python, ligera y segura
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables de entorno para optimizar Python en Docker
# PYTHONDONTWRITEBYTECODE: Evita que Python escriba archivos .pyc
# PYTHONUNBUFFERED: Asegura que los logs de la consola salgan en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 
    PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema necesarias para compilar pyswisseph
# (gcc y build-essential son necesarios para librerías en C)
RUN apt-get update 
    && apt-get install -y --no-install-recommends gcc build-essential 
    && apt-get clean 
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero el archivo de requerimientos para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip 
    && pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Exponemos el puerto 8000 (el default de FastAPI)
EXPOSE 8000

# Comando para ejecutar la aplicación
# Usamos --host 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
