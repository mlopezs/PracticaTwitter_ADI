wget apache.rediris.es/pig/pig-0.17.0/pig-0.17.0.tar.gz
tar ­-xzf pig-0.17.0.tar.gz
mv pig-0.17.0 /home/pig                                        
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop/
export PIG_CLASSPATH=$HADOOP_CONF_DIR

export PATH=$PATH:$HADOOP_HOME/bin:$JAVA_HOME/bin                   
mv home/hadoop/etc/hadoop home/hadoop/etc/hadoop_local
cp enviroment/setup/hadoop_pseudo.zip /home/hadoop/etc/hadoop
unzip /home/hadoop/etc/hadoop/hadoop_pseudo.zip
ln ­sf /home/hadoop/etc/hadoop/hadoop_pseudo /home/hadoop/etc/hadoop/hadoop

