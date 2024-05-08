# Usa la imagen python:3.9-slim como base
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Expone el puerto 8080 para la aplicación
EXPOSE 8080

# Copia los archivos necesarios al contenedor
COPY requirements.txt /app
COPY app.py /app
COPY .env /app
COPY db.sql /app   

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
