# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y la aplicación
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY static/ static/    
COPY templates/ templates/
COPY module/ module/

# Instala ffmpeg y las dependencias Python, crea directorios de salida
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && mkdir -p /app/download /app/music

# Expone el puerto 5000
EXPOSE 5000

CMD ["python3", "app.py"]


