FROM debian:latest
LABEL maintainer="Alf"

# Para copiar, Un poco obvio ¿no?
COPY ./ enviroment/
COPY $PIG_HOME /home/
COPY $HADOOP_HOME /home/hadoop/
COPY $FLUME_HOME /home/flume/

# Ejecuta cosas la primera vez que la construyo
RUN  apt-get update && apt-get install -y python2.7 &&      \
     apt-get install -y python-pip &&                       \
     apt-get install -y default-jre default-jdk &&          \
     cat enviroment/variables_entorno.txt >> root/.bashrc   
    
     

# Expone un puerto, el protocolo es opcional
EXPOSE 8080

# Ejecuta un comando, se pueden poner todos los que quieras, pero 
# solo se ejecutara el ultimo que pongas
CMD cd enviroment && pip install -r requirements.txt && make run-api

