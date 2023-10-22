#FROM python:3.12.0-alpine3.18
#FROM ubuntu:latest

# WORKDIR /app/

# COPY . .

# RUN apt -f install -y
# RUN apt-get install -y wget
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

# RUN apt-get update \
#     && apt-get install wget unzip zip -y
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install ./google-chrome-stable_current_amd64.deb -y    

# RUN pip install -r requirements.txt

# CMD ["python", "/app/seleniumTest.py"]

############################

# RUN apk update && apk add wine xauth xvfb

# RUN Xvfb :0 -screen 0 1024x768x16 &

# ENV DISPLAY=:0.0

# RUN adduser -D user

# USER user

# RUN wget -O MicrosoftEdgeSetup.exe.exe https://go.microsoft.com/fwlink/?linkid=2108834&Channel=Stable&language=es&brand=M100
# RUN wine MicrosoftEdgeSetup.exe

# RUN pip install -r requirements.txt

# CMD ["python", "/app/main.py"]

############################

# RUN apt-get update && apt-get install -y python3 python3-pip xvfb libxi6 libgconf-2-4 unzip curl
# RUN mkdir -p /msedgedriver
# WORKDIR /msedgedriver
# RUN curl -L -o msedgedriver.zip https://msedgedriver.azureedge.net/latest/MicrosoftEdgeDriver.zip
# RUN unzip msedgedriver.zip
# RUN chmod +x msedgedriver
# RUN ln -s /msedgedriver/msedgedriver /usr/local/bin/msedgedriver

##########################

# Utiliza una imagen base con sistema operativo Linux (puedes ajustar la imagen base según tus necesidades)
FROM ubuntu:20.04

# Actualiza el sistema y instala paquetes necesarios
#RUN apt-get update -y && apt-get install curl gnupg -y && apt-get install -y --reinstall software-properties-common
#RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && add-apt-repository https://packages.microsoft.com/ubuntu/20.04/prod
RUN apt-get update -y 
RUN apt-get install wget gnupg -y 
RUN apt-get install xvfb -y
RUN apt-get install -y --reinstall software-properties-common
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
RUN apt-get update -y
RUN apt-get install -y microsoft-edge-stable
RUN apt-get update -y && apt-get install -y python3 python3-pip zip unzip && \
    microsoft-edge --version

# Instala Selenium y Microsoft Edge WebDriver
#RUN pip3 install selenium
#RUN wget https://msedgedriver.azureedge.net/LATEST_RELEASE -O /tmp/msedgedriver-latest-version && \

RUN wget https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/118.0.2088.61/edgedriver_linux64.zip -P /tmp && \
    unzip /tmp/edgedriver_linux64.zip -d /usr/bin && \
    chmod +x /usr/bin/msedgedriver

#ENV PATH="/usr/bin:${PATH}"

# Define un directorio de trabajo
WORKDIR /app

# Copia tu código y archivos necesarios a la imagen
COPY . .

RUN pip3 install -r requirements.txt

# Comando para ejecutar tu script (por ejemplo, script.py)
CMD ["python3", "src/main.py"]
