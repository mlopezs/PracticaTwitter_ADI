wget apache.rediris.es/hadoop/core/hadoop-2.9.1/hadoop-2.9.1.tar.gz 
echo "Descomprimiendo archivos"
tar -xzf hadoop-2.9.1.tar.gz
echo "Copiando archivos a /home/hadoop"
mv hadoop-2.9.1/ /home/hadoop
echo "Añadiendo variables de entorno"
export HADOOP_HOME=/home/hadoop/
export JAVA_HOME=/usr/lib/jvm/java8openjdkamd64/
export PATH=$PATH:$HADOOP_HOME/bin:$JAVA_HOME/bin
echo "Duplicando directorios de hadoop"
cp -r home/hadoop/etc/hadoop home/hadoop/etc/hadopp_local
ls home/hadoop/etc/
echo "Copiando configuracion a hadoop"
cp enviroment/setup/hadoop_pseudo.zip /home/hadoop/etc/hadoop
echo "Descomprimiendo configuracion"
unzip /home/hadoop/etc/hadoop/hadoop_pseudo.zip
echo "Creando enlace simbolico"
ln -sf /home/hadoop/etc/hadoop/hadoop_pseudo /home/hadoop/etc/hadoop