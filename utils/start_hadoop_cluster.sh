#!/bin/bash

hdfs namenode -format
$HADOOP_HOME/sbin/start-yarn.sh && $HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver
hdfs dfs -mkdir -p /user/tweets-collect
hdfs dfs -mkdir /user/storage
echo
jps
