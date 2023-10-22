# Utiliza una imagen base con sistema operativo Linux (puedes ajustar la imagen base según tus necesidades)
FROM ubuntu:20.04

# Actualiza el sistema y instala paquetes necesarios
RUN apt-get update -y 
RUN apt-get install -y --reinstall software-properties-common
RUN apt-get install wget gnupg python3 python3-pip zip unzip -y 
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
RUN apt-get update -y
RUN apt-get install -y microsoft-edge-stable

# Instala Microsoft Edge WebDriver
RUN wget https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/118.0.2088.61/edgedriver_linux64.zip -P /tmp && \
    unzip /tmp/edgedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/msedgedriver

# Define un directorio de trabajo
WORKDIR /app

# Copia tu código y archivos necesarios a la imagen
COPY . .

RUN pip3 install -r requirements.txt

# Comando para ejecutar tu script (por ejemplo, script.py)
CMD ["python3", "src/main.py"]
